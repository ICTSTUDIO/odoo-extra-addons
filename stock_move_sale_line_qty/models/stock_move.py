# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_ordered = fields.Float(
            compute="_get_order_qty",
            digits=dp.get_precision('Product Unit of Measure'),
            string='Ordered',
            help="Quantity Ordered"
    )

    @api.model
    def _get_real_ordered_qty(self):
        return self.sale_line_id.product_uom_qty

    @api.one
    @api.depends('sale_line_id')
    def _get_order_qty(self):
            self.qty_ordered = self._get_real_ordered_qty()
