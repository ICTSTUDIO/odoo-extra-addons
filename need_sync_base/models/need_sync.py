# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSync(models.Model):
    _name = "need.sync"
    _description = "Need Sync Base Model"

    def _select_models(self):
        return self.env['need.sync.model']._select_models()


    name = fields.Char(
            string="Sync",
            compute="_get_name",
            store=True
    )
    model = fields.Selection(
            selection=_select_models,
            string="Model",
            required=True,
            index=True
    )
    res_id = fields.Integer(
            string='Record ID',
            index=True,
            required=True,
            help="ID of the target record in the database"
    )
    record = fields.Reference(
            selection=_select_models,
            string="Record",
            compute="_get_record",
            store=True,
            size=128
    )
    need_sync_date = fields.Datetime(
            string="Need Sync Datetime"
    )
    sync_lines = fields.One2many(
            comodel_name="need.sync.line",
            inverse_name="need_sync",
            string="Sync Lines"
    )

    @api.multi
    @api.depends('res_id', 'model')
    def _get_record(self):
        for rec in self:
            if rec.res_id and rec.model:
                rec.record = rec.env[str(rec.model)].browse(rec.res_id)

    @api.multi
    @api.depends('res_id', 'model')
    def _get_name(self):
        for rec in self:
            object = rec.env[rec.model].browse(rec.res_id)
            if object and 'name' in object._fields:
                object_name = object.name
            else:
                object_name = "No object name defined"
            rec.name = '%s' % (object_name)

    @api.model
    def get_model_allowed_connections(self):
        syncmodels = self.env['need.sync.connection.model'].search(
            [
                ('model', '=', self.model),
                ('auto_create_lines', '=', True)
            ]
        )
        _logger.debug("Sync Model Connnections: %s", syncmodels)
        connections = syncmodels.mapped('need_sync_connection')
        _logger.debug("Sync Connections: %s", connections)
        return connections

    @api.model
    def _autocreate_syncline_connection(self, connection):
        lines = self.sync_lines
        cline = lines.filtered(lambda l: l.need_sync_connection.id ==connection.id)
        if not cline:
            self.env['need.sync.line'].create(
                {
                    'need_sync_connection': connection.id,
                    'need_sync': self.id
                }
            )

    @api.multi
    def _autocreate_sync_lines(self):
        for rec in self:
            if rec.model:
                connections = rec.get_model_allowed_connections()
                for connection in connections:
                    _logger.debug("Autocreate for Conncetion: %s", connection)
                    rec._autocreate_syncline_connection(connection)


    @api.multi
    def set_need_sync(self, model, res_ids):
        """
        Pass need sync to model and resources
        :param model: need sync on wich model
        :param res: list of resources to set sync
        :return: boolean True or False
        """

        if isinstance(res_ids, (long, int)):
            res_ids = [res_ids]

        # Get list of IDS where a record in need sync exists
        # and a list for creating a need sync record
        need_syncs = self.search(
                [
                    ('model', '=', model),
                    ('res_id', 'in', res_ids)
                ]
        )
        need_syncs.write({
            'need_sync_date': fields.Datetime.now()
        }
        )
        # Need sync res_ids list
        need_sync_res_ids = [x.res_id for x in need_syncs]
        create_sync_ids = list(set(res_ids) - set(need_sync_res_ids))

        if create_sync_ids:
            _logger.debug("Create new Need sync records")
            created_need_syncs = self._create_need_sync(model, create_sync_ids)
            need_syncs = need_syncs | created_need_syncs

        # Check if all lines exist for autocreate models
        _logger.debug("Need Syncs Autocreate Check: %s", need_syncs)
        need_syncs._autocreate_sync_lines()

    @api.model
    def _create_need_sync(self, model, res_ids):
        return_need_syncs = self.env['need.sync']
        if model and res_ids:
            for res_id in res_ids:
                create_need_sync = self.create(
                        {
                            'model': model,
                            'res_id': res_id,
                            'need_sync_date': fields.Datetime.now()
                        }
                )
                _logger.debug("Need Sync Created: %s", create_need_sync)
                return_need_syncs = return_need_syncs | create_need_sync

        return return_need_syncs

    @api.model
    def unlink_records(self, model, res_ids):
        '''
        When calling unlink of a used model record, call this method to remove
        the linked need syncs.
        :param model: Model
        :param res_ids: List of ids
        :return: True
        '''
        need_syncs = self.search(
            [
                ('model', '=', model),
                ('res_id', 'in', res_ids)
            ]
        )
        if need_syncs:
            need_syncs.unlink()
        return True