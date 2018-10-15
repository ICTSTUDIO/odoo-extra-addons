# -*- coding: utf-8 -*-
# Copyright© 2017-today ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    label_incoming = fields.Boolean(
        string="Label Incoming Stock",
        default=False
    )
    label_outgoing = fields.Boolean(
        string="Label Outgoing Stock",
        default=False
    )
