# -*- coding: utf-8 -*-
# Copyright© 2017-today ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def print_labels(self):
        return self.product_variant_ids.print_labels()

    @api.multi
    def print_labels_medium(self):
        return self.product_variant_ids.print_labels_medium()

    @api.multi
    def print_labels_small(self):
        return self.product_variant_ids.print_labels_small()