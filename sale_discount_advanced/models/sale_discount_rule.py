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

class SaleDiscountRule(models.Model):
    _name = 'sale.discount.rule'
    _order = 'sequence'

    company_id = fields.Many2one(
            comodel_name='res.company',
            string='Company',
            required=True,
            default=lambda self: self.env.user.company_id
    )
    sequence = fields.Integer("Sequence")
    sale_discount_id = fields.Many2one(
            comodel_name='sale.discount',
            string="Discount",
            required=True
    )

    discount_type = fields.Selection(
        [
            ('perc', 'Percentage'),
            ('amnt', 'Amount')
        ],
        string='Type of Discount'
    )
    discount = fields.Float('Discount amount')

    max_base = fields.Float("Max base amount")

    @api.one
    @api.constrains('discount', 'discount_type')
    def _check_sale_discount(self):
        # Check if amount is positive
        if self.discount < 0:
            raise ValidationError(
                    "Discount Amount needs to be a positive number"
            )
        # Check if percentage is between 0 and 100
        elif self.discount_type == 'rel' and self.discount > 100:
            raise ValidationError(
                    "Relative discount must be between 0 and 100."
            )
