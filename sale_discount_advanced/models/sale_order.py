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


    discount_amount = fields.Float(
            compute='_compute_discount',
            string="Total Discount Amount",
            store=True
    )
    discount_base_amount = fields.Float(
            compute='_compute_discount',
            string="Order Amount before Discount",
            store=True
    )

    def _get_active_discounts(self):
        discounts = []
        if self.pricelist_id and self.pricelist_id.sale_discounts:
            for discount in self.pricelist_id.sale_discounts:
                if discount.active and \
                        discount.check_active_date(self.date_order):
                    discounts.append(discount)
        _logger.debug("Active Discounts: %s", discounts)
        return discounts


    @api.one
    @api.depends('pricelist_id','partner_id','order_line')
    def _compute_discount(self):

        order_id =self.id
        _logger.debug('Order_id: %s', self.id)
        grouped_discounts = {}
        sale_discount_order_lines = []
        _logger.debug('Compute Discount')
        _logger.debug(self.env.context)
        if not self.env.context.get('discount_calc'):
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

            total_discount_amount = 0.0
            total_discount_base_amount = 0.0

            for discount in grouped_discounts.values():
                discount['amount'] = discount['sale_discount']._calculate_discount(discount['discount_base'], discount['discount_qty'])
                if not discount['amount']:
                    continue

                order_line_values = {
                    'order_id': order_id,
                    'sale_discount_line': True,
                    'name': discount['sale_discount'].name,
                    'product_id': discount['sale_discount'].product_id.id,
                    'price_unit': -discount['amount'],
                    'product_uom_qty': 1
                }

                ctx = dict(self._context, discount_calc=True)

                _logger.debug('Vals: %s', order_line_values)
                exists, equal = self.order_line.with_context(ctx).existing_discountline(order_line_values)
                if exists and not equal:
                    exists.with_context(ctx).write(order_line_values)
                elif not exists and not equal:
                    self.order_line.with_context(ctx).create(order_line_values)


                total_discount_amount += discount['amount'] or 0.0
                total_discount_base_amount = discount['discount_base']

            self.discount_amount = total_discount_amount
            self.discount_base_amount = total_discount_base_amount
