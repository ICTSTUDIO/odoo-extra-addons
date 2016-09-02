# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ERP|OPEN (www.erpopen.nl).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    calc_costprice = fields.Boolean(
        string="Calculate Costrpice",
        default=False,
        help="Mark this True when you want to Calculate the Realtime stock Value based on a Factor from the Sale Price"

    )
    calc_costprice_factor = fields.Float(
        string="Costprice Factor",
        default=1.0,
        help="Calculation used: sale price / factor = valuation value"
    )

    # @api.onchange('factor')
    # def _calculate_costprice(self):
    #
    #     if self.list_price != 0 and self.factor != 0:
    #         self.standard_price =  self.list_price / self.factor
