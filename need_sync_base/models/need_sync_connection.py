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

    _sql_constraints = {
        ('connection_uniq', 'unique(connection)', 'Connection needs to be unique')
    }

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