# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

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
        if self.last_check_date:
            return self.env[self.model].search(
                    [
                        ('write_date', '>', self.last_check_date)
                    ]
            )
        else:
            return self.env[self.model].search([])

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