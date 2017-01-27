# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp import models, fields, api

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

    @api.one
    @api.depends('res_id', 'model')
    def _get_record(self):
        if self.res_id and self.model:
            print self.res_id
            print self.model
            self.record = self.env[str(self.model)].browse(self.res_id)

    @api.one
    @api.depends('res_id', 'model')
    def _get_name(self):
        object = self.env[self.model].browse(self.res_id)
        if object and 'name' in object._fields:
            object_name = object.name
        else:
            object_name = "No object name defined"
        self.name = '%s' % (object_name)

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
            self._create_need_sync(model, create_sync_ids)

    @api.model
    def _create_need_sync(self, model, res_ids):
        if model and res_ids:
            for res_id in res_ids:
                create_need_sync = self.create(
                        {
                            'model': model,
                            'res_id': res_id,
                            'need_sync_date': fields.Datetime.now()
                        }
                )
                if create_need_sync:
                    for connection_model in self.env['need.sync.connection.model'].search(
                            [
                                ('model', '=', model)
                            ]
                    ):
                        self.env['need.sync.line']._auto_create_need_sync(
                                create_need_sync,
                                connection_model.need_sync_connection
                        )

