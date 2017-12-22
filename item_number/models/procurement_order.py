# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    item_number = fields.Char(string='Item Number')

    @api.model
    def _run_move_create(self, procurement):
        vals = super(ProcurementOrder, self)._run_move_create(procurement)
        vals['item_number'] = procurement.item_number
        return vals