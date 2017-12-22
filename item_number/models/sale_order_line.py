# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _order = 'item_number'

    item_number = fields.Char(string='Item Number')

    @api.model
    def _prepare_order_line_invoice_line(self, line, account_id=False):
        vals = super(SaleOrderLine, self)._prepare_order_line_invoice_line(line, account_id=account_id)
        vals['item_number'] = line.item_number
        return vals
