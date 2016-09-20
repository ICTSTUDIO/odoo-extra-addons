# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    stock_product_location_ids = fields.One2many(
            comodel_name='stock.product.location',
            inverse_name='product_id',
            string='Location Stock '
    )

    @api.one
    def copy(self, default=None):
        default = dict(default or {})

        default['stock_product_location_ids'] = []

        return super(ProductProduct, self).copy(default)