# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
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
