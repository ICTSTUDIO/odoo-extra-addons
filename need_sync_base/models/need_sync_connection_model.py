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


class NeedSyncConnectionModel(models.Model):
    _name = "need.sync.connection.model"
    _description = "Need Sync Connection Models"
    _rec_name = 'model'

    def _select_models(self):
        return self.env['need.sync.model']._select_models()

    model = fields.Selection(
            selection=_select_models,
            string="Model",
            required=True,
            index=True
    )
    need_sync_connection = fields.Many2one(
            comodel_name="need.sync.connection",
            string="Connection",
            index=True
    )

    _sql_constraints = {
        ('connection_model_uniq', 'unique(model, need_sync_connection)', 'Only one model per connection')
    }
