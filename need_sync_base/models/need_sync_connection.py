# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncConnection(models.Model):
    _name = "need.sync.connection"
    _description = "Need Sync Connection Based"

    def _select_models(self):
        return []

    name = fields.Char(
            string="Sync",
            compute="_get_name",
            store=True
    )
    connection = fields.Reference(
        string="Connection",
        selection=_select_models,
        required=True,
        size=128
    )
    use_confirm_date = fields.Boolean(
        string="Use Confirmation Date",
        default=False
    )
    allowed_models=fields.One2many(
        comodel_name="need.sync.connection.model",
        inverse_name="need_sync_connection",
        string="Allowed Models"
    )
    published = fields.Boolean(
        compute="_get_published",
        #inverse="_set_published",
        string="Published"
    )

    _sql_constraints = {
        ('connection_uniq', 'unique(connection)', 'Connection needs to be unique')
    }

    def _set_published(self):
        """
        Hook to trigger editable field
        :return: 
        """
        return True

    @api.model
    def check_res_model(self, res_id, model):
        return res_id, model

    @api.model
    def check_unpublished(self, res_id, model):
        unpublished = self.env['need.sync.connection.record.exception'].search(
            [
                ('res_id', '=', res_id),
                ('model', '=', model),
                ('need_sync_connection', '=', self.id)
            ]
        )
        if unpublished:
            return True
        else:
            return False

    @api.one
    def _get_published(self):
        _logger.debug("Context: %s", self._context)
        if self._context.get('active_id') and self._context.get('active_model'):
            res_id, model = self.check_res_model(self._context.get('active_id'), self._context.get('active_model'))
            _logger.debug("Res_id: %s, Model: %s", res_id, model)
            if self.check_unpublished(res_id, model):
                self.published = False
            else:
                self.published = True
        else:
            self.published = True


    @api.one
    @api.depends('connection')
    def _get_name(self):
        if self.connection and 'name' in self.connection._fields:
            self.name = '%s' % (self.connection.name)
        else:
            self.name = '%s' % ('No Connection Name')

    @api.model
    def get_need_sync_list(self, model):
        return self.env['need.sync.line'].search(
                [
                    ('need_sync_connection', '=', self.id),
                    ('model', '=', model),
                    ('sync_needed', '=', True)
                ]
        )

    @api.model
    def map_need_sync(self, model, res_ids):
        return self.env['need.sync.line'].map_need_sync(model, res_ids, self)

    @api.model
    def set_published(self, res_id, model, published, dest_model=None):
        _logger.debug("ConnectionID: %s, Published: %s", self.id, published)
        if dest_model and model != dest_model:
            res_id, model = self.check_res_model(res_id, model)
        if dest_model and model == dest_model or model:
            unpublished = self.env['need.sync.connection.record.exception'].search(
                [
                    ('res_id', '=', res_id),
                    ('model', '=', model),
                    ('need_sync_connection', '=', self.id)
                ]
            )

            if published and unpublished:
                unpublished.unlink()
            elif not published and not unpublished:
                self.env['need.sync.connection.record.exception'].create(
                    {
                        'res_id': res_id,
                        'model': model,
                        'need_sync_connection': self.id
                    }
                )

    @api.model
    def get_dest_model(self, active_model):
        return False

    @api.one
    def manual_unpublish(self):
        if self._context.get('active_id') and self._context.get('active_model'):
            dest_model = self.get_dest_model(self._context.get('active_model'))
            self.set_published(self._context.get('active_id'), self._context.get('active_model'), False, dest_model=dest_model)

    @api.one
    def manual_publish(self):
        if self._context.get('active_id') and self._context.get('active_model'):
            dest_model = self.get_dest_model(self._context.get('active_model'))
            self.set_published(self._context.get('active_id'), self._context.get('active_model'), True, dest_model=dest_model)