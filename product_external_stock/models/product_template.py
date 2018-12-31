# -*- coding: utf-8 -*-
# Copyright© 2017-today ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    external_stock = fields.Boolean(string="Use External Stock")
    external_stock_qty = fields.Float(string="External Stock Qty")