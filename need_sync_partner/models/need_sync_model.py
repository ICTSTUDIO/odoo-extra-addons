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


class NeedSyncModel(models.Model):
    _inherit = "need.sync.model"

    def _select_models(self):
        list_models = super(NeedSyncModel, self)._select_models()
        list_models.append(('res.partner', 'Partner'))
        return list_models

    model = fields.Selection(
            selection=_select_models,
            string="Model",
            required=True,
            index=True
    )

    @api.multi
    def get_object_records_changed(self):
        """
        Detect Object Changes
        :return: list of res_id
        """
        self.ensure_one()

        changed_records = super(NeedSyncModel, self).get_object_records_changed()
        if self.model == 'res.partner':

            changed_records = self.env['res.partner'].search(
                    [
                        ('write_date', '>', self.last_check_date),
                    ]
            )
        return changed_records
