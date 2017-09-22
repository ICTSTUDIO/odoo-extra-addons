# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncModel(models.Model):
    _inherit = "need.sync.model"

    def _select_models(self):
        list_models = super(NeedSyncModel, self)._select_models()
        list_models.append(('res.partner', 'Partners'))
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
            if changed_records:
                parent_records = changed_records.mapped('parent_id')
                changed_records = changed_records | parent_records
                child_records = self.env['res.partner'].search(
                        [
                            ('parent_id', 'in', changed_records.ids),
                            ('write_date', '>', self.last_check_date)
                        ]
                )
                changed_records | changed_records | child_records

        return changed_records
