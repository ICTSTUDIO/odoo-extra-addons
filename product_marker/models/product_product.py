# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    marker_ids = fields.Many2many(
            comodel_name="product.marker",
            relation="product_product_marker_rel",
            column1="product_id",
            column2="marker_id",
            string="Markers"
    )
