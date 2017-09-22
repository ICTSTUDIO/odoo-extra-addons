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
        list_models.append(('product.public.category', 'Product Public Category'))
        return list_models

    model = fields.Selection(
            selection=_select_models,
            string="Model",
            required=True,
            index=True
    )