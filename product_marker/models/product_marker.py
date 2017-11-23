# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class ProductMarker(models.Model):
    _name = "product.marker"

    name = fields.Char(
            string="Marker",
            required=True,
            size=128
    )
    product_ids = fields.Many2many(
            comodel_name="product.product",
            relation="product_product_marker_rel",
            column1="marker_id",
            column2="product_id",
            string="Products"
    )
