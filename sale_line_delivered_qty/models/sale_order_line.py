# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_delivered = fields.Float(
            compute="_get_pick_qty",
            digits=dp.get_precision('Product Unit of Measure'),
            string='Delivered',
            store=True,
            help="Quantity Delivered"
    )

    @api.model
    def check_move(self, move):
        if move.state != 'done':
            return False
        if all([self._context.get('date_start'), self._context.get('date_stop')]):
            if not (move.date >= self._context['date_start'] and
                            move.date <= self._context['date_stop']):
                return False
        return True

    @api.model
    def _get_real_move_qty(self, move):
        src = move.location_id.usage
        dst = move.location_dest_id.usage

        if src == dst:
            return 0.0
        elif src == 'internal':
            return self.product_uom._compute_qty_obj(
                    move.product_uom,
                    move.product_qty,
                    self.product_uom)
        elif dst == 'internal':
            return -self.product_uom._compute_qty_obj(
                    move.product_uom,
                    move.product_qty,
                    self.product_uom)
        else:
            return 0.0

    @api.one
    @api.depends('move_ids.state')
    def _get_pick_qty(self):
            qty_delivered = 0
            for move in self.move_ids:
                if self.check_move(move):
                    # Add Quantity
                    qty_delivered += self._get_real_move_qty(move)
                    _logger.debug("Qty Delivered: %s", qty_delivered)
            self.qty_delivered = qty_delivered
