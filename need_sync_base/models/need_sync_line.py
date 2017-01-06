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


class NeedSyncLine(models.Model):
    _name = "need.sync.line"
    _description = "Need Sync Line Based"

    name = fields.Char(
            string="Sync",
            compute="_get_name"
    )
    need_sync = fields.Many2one(
            comodel_name="need.sync",
            string="Need Sync",
            index=True
    )
    need_sync_connection = fields.Many2one(
            comodel_name="need.sync.connection",
            string="Connection",
            index=True
    )
    need_sync_date = fields.Datetime(
            related="need_sync.need_sync_date"
    )
    model = fields.Selection(
            related="need_sync.model"
    )
    res_id = fields.Integer(
            related="need_sync.res_id"
    )
    record = fields.Reference(
            related="need_sync.record"
    )
    sync_needed = fields.Boolean(
            string="Sync Needed",
            compute="_compute_need_sync",
            store=True,
            index=True,
            help="Synchronization Required"
    )
    last_sync_date = fields.Datetime(
            string="Last Sync Datetime"
    )
    confirmed_date = fields.Datetime(
            string="Last Sync Datetime"
    )

    _sql_constraints = {
        ('connection_need_sync_uniq', 'unique(need_sync, need_sync_connection)', 'Only one need sync per connection')
    }

    @api.one
    @api.depends('need_sync.res_id',
                 'need_sync.model',
                 'need_sync_connection.name'
                 )
    def _get_name(self):
        object = self.env[self.need_sync.model].browse(self.need_sync.res_id)
        if object and 'name' in object._fields:
            object_name = object.name
        else:
            object_name = "No object name defined"
        if self.need_sync_connection:
            connection_name = self.need_sync_connection.name
        else:
            connection_name = 'No Connection Name'
        self.name = '%s (%s)' % (object_name, connection_name)

    @api.one
    @api.depends('need_sync.need_sync_date',
                 'last_sync_date',
                 'confirmed_date'
                 )
    def _compute_need_sync(self):
        if self.need_sync_date > self.last_sync_date:
            self.sync_needed = True
        elif self.need_sync_date and not self.last_sync_date:
            self.sync_needed = True
        elif self.sync_needed == True:
            self.sync_needed = False

    @api.multi
    def _create_need_sync(self, need_sync, need_sync_connection):
        if need_sync and need_sync_connection:
            self.create(
                    {
                        'need_sync': need_sync.id,
                        'need_sync_connection': need_sync_connection.id
                    }
            )