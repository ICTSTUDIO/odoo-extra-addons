# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    stock_product_location_ids = fields.One2many(
            related='product_variant_ids.stock_product_location_ids',
            string='Location Stock'
    )