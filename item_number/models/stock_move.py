# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'
    _order = 'item_number'

    item_number = fields.Char(string='Item Number')

    @api.model
    def _get_invoice_line_vals(self, move, partner, inv_type):
        '''Add Item Number to the invoice vals for correct invoicing'''
        res = super(StockMove, self)._get_invoice_line_vals(move, partner, inv_type)
        res['item_number'] = move.item_number or 0
        return res