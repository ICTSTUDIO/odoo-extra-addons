# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncConnectionRecordException(models.Model):
    _name = "need.sync.connection.record.exception"
    _description = "Need Sync Connection Records Not synced"

    def _select_models(self):
        return self.env['need.sync.model']._select_models()

    name = fields.Char(
        string="Sync",
        compute="_get_name",
        store=True
    )

    need_sync_connection = fields.Many2one(
        comodel_name="need.sync.connection",
        string="Connection",
        index=True
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
        store=True
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

    def unlink(self):
        """
        Recreate related need sync line
        :return: 
        """
        res_ids = []
        for rec in self:
            res_ids.append(rec.res_id)
        need_sync_lines = self.get_need_sync_lines(
            res_ids,
            self[0].model,
            self[0].need_sync_connection.id
        )
        if need_sync_lines:
            need_sync_lines.write({'published': True})
        return super(NeedSyncConnectionRecordException, self).unlink()


    def create(self, values):
        """
        Remove related need sync lines
        :return: 
        """
        if values.get('res_id') and values.get('model') and values.get('need_sync_connection'):
            need_sync_lines = self.get_need_sync_lines(
                values.get('res_id'),
                values.get('model'),
                values.get('need_sync_connection')
            )
            if need_sync_lines:
                need_sync_lines.write({'published': False})
        return super(NeedSyncConnectionRecordException, self).create(values)

    @api.model
    def get_need_sync_lines(self, res_ids, model, connection_id):
        if isinstance(res_ids, (long, int)):
            res_ids = [res_ids]

        need_sync_lines = self.env['need.sync.line'].search(
            [
                ('res_id', 'in', res_ids),
                ('model', '=', model),
                ('need_sync_connection', '=', connection_id)

            ]
        )
        return need_sync_lines
