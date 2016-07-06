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

class SaleDiscount(models.Model):
    _name = "sale.discount"

    company_id = fields.Many2one(
            comodel_name='res.company',
            string='Company',
            required=True,
            default=lambda self: self.env.user.company_id
    )
    name = fields.Char(
            string="Discount",
            required=True
    )
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    active = fields.Boolean(
        string='Discount active',
        default=lambda self: self._get_default_active()
    ) #  TODO: Change default with lambda function
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Discount Product",
        help="This product will be used to create lines on order regarding discount"
    )
    discount_base = fields.Selection(
        selection=[
            ('sale_order', 'Base discount on Order amount'),
            ('sale_line', 'Base discount on Line amount')
        ],
        string="Discount Base on",
        required=True,
        help="Base the discount on "
    )

    pricelists = fields.Many2many(
            comodel_name='product.pricelist',
            relation='pricelist_sale_discount_rel',
            column1='discount_id',
            column2='pricelist_id',
            string="Pricelists"
    )

    rules = fields.One2many(
            comodel_name='sale.discount.rule',
            inverse_name='sale_discount_id',
            string="Discount Rules"
    )

    # sale_discounts = fields.Many2many(
    #         comodel_name='sale.order.line',
    #         relation='sale_line_sale_discount_rel',
    #         column1='discount_id',
    #         column2='sale_line_id',
    #         string="Order Lines"
    # )

    def _get_default_active(self):
        return True

    def check_active_date(self, check_date=None):
        if not check_date:
            check_date = fields.Datetime.now()
        if self.start_date and self.end_date and (check_date >= self.start_date and check_date < self.end_date):
            return True
        if self.start_date and not self.end_date and (check_date >= self.start_date):
            return True
        if not self.start_date and self.end_date and (check_date < self.end_date):
            return True
        elif not self.start_date or not self.end_date:
            return True
        else:
            return False

    @api.multi
    def _calculate_discount(self, base, qty):
        assert len(self) == 1
        for discount in self:
            for rule in discount.rules:
                if rule.max_base > 0 and rule.max_base > base:
                    _logger.debug("No Discount")
                    continue

                if rule.discount_type == 'perc':
                    _logger.debug("Calculate Discount Perc")
                    return base * rule.discount / 100
                else:
                    _logger.debug("Calculate Discount Amount")
                    return min(rule.discount * qty, base)
