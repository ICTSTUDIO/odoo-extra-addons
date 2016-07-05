# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_amount = fields.Float(compute='_compute_discount')
    def _get_active_discounts(self):
        discounts = []
        if self.pricelist_id and self.pricelist_id.sale_discounts:
            for discount in self.pricelist_id.sale_discounts:
                if discount.active and discount.check_active_date(self.date_order):
                    discounts.append(discount)
        _logger.debug("Active Discounts: %s", discounts)
        return discounts


    @api.depends('order_line')
    def _compute_discount(self):
        # if not self.env.context.get('discount_calc'):
        #     active_discounts = self._get_active_discounts()
        #
        grouped_discounts = {}
        sale_discount_order_lines = []
        for line in self.order_line:
            if line.sale_discount_line:
                _logger.debug("Sale Line With Discount: %s", line.id)
                sale_discount_order_lines.append((2, line.id))
                continue

            line_sale_discounts = []
            for discount in line.sale_discounts:
                line_sale_discounts.append(discount)
                grouped_discounts.setdefault(discount.id,
                                             {
                                                 'sale_discount': discount,
                                                 'discount_base': 0,
                                                 'amount': 0,
                                                 'discount_qty': 0
                                             }
                                             )
                grouped_discounts[discount.id]['discount_base'] += line.price_subtotal
                grouped_discounts[discount.id]['discount_qty'] += line.product_uom_qty
            # _logger.debug("Write Discounts on line: %s", line_sale_discounts)
            # line.with_context({'discount_calc': True}).write({'sale_discounts': [(6, 0, [ld.id for ld in line_sale_discounts])]})


        for discount in grouped_discounts.values():
            discount['amount'] = discount['sale_discount']._calculate_discount(discount['discount_base'], discount['discount_qty'], self)
            if not discount['amount']:
                continue

            sale_discount_order_lines.append((0,0,{
                'order_id': self.id,
                'sale_discount_line': True,
                'name': discount['sale_discount'].name,
                'product_id': discount['sale_discount'].product_id.id,
                'price_unit': discount['amount'],
                'product_uom_qty': -1
            }))

        _logger.debug("Write Order Line: %s", sale_discount_order_lines)
        if sale_discount_order_lines:
            self.order_line.with_context({'discount_calc': True}).write(sale_discount_order_lines)

