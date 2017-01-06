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
    _name = "need.sync.model"
    _description = "Need Sync Base Model"
    _rec_name='model'

    def _select_models(self):
        return []

    model = fields.Selection(
            selection=_select_models,
            string="Model",
            required=True,
            index=True
    )
    last_check_date = fields.Datetime(
            string="Last Check Datetime"
    )

    _sql_constraints = {
        ('model_uniq', 'unique(model)', 'Model needs to be unique')
    }

    @api.multi
    def get_object_records_changed(self):
        """
        Detect Object Changes
        :return: list of res_id
        """
        self.ensure_one()
        return self.env[self.model].search(
                [
                    ('write_date', '>', self.last_check_date)
                ]
        )

    @api.multi
    def get_object_ids_changed(self):
        """
        Detect Object Changes
        :return: list of res_id
        """
        changed_records = self.get_object_records_changed()
        if changed_records:
            return changed_records.ids
        return []

    @api.model
    def check_models(self):
        for rec in self.search([]):
            rec._check_models()

    @api.multi
    def _check_models(self):
        for rec in self:
            changed_ids = rec.get_object_ids_changed()
            if changed_ids:
                rec.env['need.sync'].set_need_sync(rec.model, changed_ids)
                rec.last_check_date = fields.Datetime.now()