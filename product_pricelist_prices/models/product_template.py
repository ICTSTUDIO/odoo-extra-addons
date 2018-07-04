# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def get_pricelists(self):
        for rec in self:
            rec._get_pricelists()

    @api.multi
    def _get_pricelists(self):
        self.pricelists = self.env['product.pricelist'].search(
                [
                    ('show_on_products', '=', True)
                ]
        )

    def _set_pricelists(self):
        for pricelist in self.pricelists:
            if pricelist.product_price:
                _logger.debug("Updating Price: %s", pricelist.product_price)
                pricelist.price_set(self, pricelist.product_price)
    
    pricelists = fields.One2many(
            comodel_name="product.pricelist",
            string="Pricelists",
            compute="get_pricelists",
            inverse="_set_pricelists"
    )
