# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def _get_product_phantom_bom_qty(self, move):
        bom_obj = self.env['mrp.bom']
        property_ids = self._context.get('property_ids') or []
        bis = bom_obj.sudo()._bom_find(product_id=self.product_id.id, properties=property_ids)
        bom_point = bom_obj.sudo().browse(bis)
        if bis and bom_point.type == 'phantom':
            processed_ids = []
            factor = self.sudo().product_uom._compute_qty_obj(self.product_uom, 1, bom_point.product_uom) / bom_point.product_qty
            res = bom_obj.sudo()._bom_explode(bom_point, self.product_id, factor, property_ids)
            for line in res[0]:
                if line['product_id'] == move.product_id.id:
                    return line['product_qty']
        return False

    @api.model
    def _get_real_move_qty(self, move):
        if self.product_id != move.product_id:
            src = move.location_id.usage
            dst = move.location_dest_id.usage

            original_product_qty = self._get_product_phantom_bom_qty(move)
            _logger.debug('Original Qty: %s', original_product_qty)


            move_qty = self.product_uom._compute_qty_obj(
                    move.product_uom,
                    move.product_qty,
                    self.product_uom)
            _logger.debug('Move Qty: %s', move_qty)
            if move_qty and original_product_qty:
                move_qty = move_qty / original_product_qty
            _logger.debug('Move Qty: %s', move_qty)

            if src == dst:
                return 0.0
            elif src == 'internal':
                return move_qty
            elif dst == 'internal':
                return -move_qty
            else:
                return 0.0
        else:
            return super(SaleOrderLine, self)._get_real_move_qty(move)


    @api.one
    def _get_pick_qty(self):
        qty_delivered = 0
        if all(self.product_id != move.product_id for move in self.move_ids) and self.move_ids:
            check_product = self.move_ids[0].product_id
            for move in self.move_ids:
                if move.product_id == check_product:
                    if self.check_move(move):
                        # Add Quantity
                        qty_delivered += self._get_real_move_qty(move)
                        _logger.debug("Qty Delivered: %s", qty_delivered)
            self.qty_delivered = qty_delivered
        else:
            super(SaleOrderLine, self)._get_pick_qty()
