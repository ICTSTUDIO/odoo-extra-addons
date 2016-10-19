# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _get_product_phantom_bom_qty(self):
        sl = self.sale_line_id
        bom_obj = self.env['mrp.bom']
        property_ids = self._context.get('property_ids') or []
        bis = bom_obj.sudo()._bom_find(product_id=sl.product_id.id, properties=property_ids)
        bom_point = bom_obj.sudo().browse(bis)
        if bis and bom_point.type == 'phantom':
            factor = self.sudo().product_uom._compute_qty_obj(sl.product_uom, sl.product_uom_qty, bom_point.product_uom) / bom_point.product_qty
            res = bom_obj.sudo()._bom_explode(bom_point, sl.product_id, factor, property_ids)
            for line in res[0]:
                if line['product_id'] == self.product_id.id:
                    return line['product_qty']
        return sl.product_uom_qty

    @api.model
    def _get_real_ordered_qty(self):
        if self.sale_line_id and self.product_id != self.sale_line_id.product_id:

            return self._get_product_phantom_bom_qty()

        else:
            return super(StockMove, self)._get_real_ordered_qty()