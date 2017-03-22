# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.one
    def _get_pricelists(self):
        self.pricelists = self.env['product.pricelist'].search(
                [
                    ('show_on_products', '=', True),
                    ('type', '=', 'sale')
                ]
        )

    def _set_pricelists(self):
        for pricelist in self.pricelists:
            if pricelist.product_price:
                _logger.debug("Updating Price: %s", pricelist.product_price)
                pricelist.price_set(self, pricelist.product_price)

    @api.one
    def _get_purchase_pricelists(self):
        self.purchase_pricelists = self.env['product.pricelist'].search(
                [
                    ('show_on_products', '=', True),
                    ('type', '=', 'purchase')
                ]
        )

    def _set_purchase_pricelists(self):
        for pricelist in self.purchase_pricelists:
            if pricelist.product_price:
                _logger.debug("Updating Price: %s", pricelist.product_price)
                pricelist.price_set(self, pricelist.product_price)
    
    pricelists = fields.One2many(
            comodel_name="product.pricelist",
            string="Pricelists",
            compute="_get_pricelists",
            inverse="_set_pricelists"
    )

    purchase_pricelists = fields.One2many(
            comodel_name="product.pricelist",
            string="Purchase Pricelists",
            compute="_get_purchase_pricelists",
            inverse="_set_purchase_pricelists"
    )
