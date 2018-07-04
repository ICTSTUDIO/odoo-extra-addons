# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class product_pricelist(models.Model):
    _inherit = 'product.pricelist'

    product_price_margin = fields.Float(
        compute="get_product_margin",
        string="Margin"
    )

    @api.depends('product_price')
    @api.multi
    def get_product_margin(self):
        for rec in self:
            rec._get_product_margin()

    @api.multi
    def _get_product_margin(self):
        margin = 0.0
        if self.product_id and self.product_price:
            product = self.env['product.product'].search([('id', '=', self.product_id)])
            if product:
                if product.standard_price:
                    margin = (self.product_price - product.standard_price) / self.product_price
                else:
                    margin = 1
        self.product_price_margin = margin

