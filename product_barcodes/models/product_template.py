# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright© 2015-2017 ERP|OPEN <http://www.erpopen.nl>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    barcode_ids = fields.One2many(
        related='product_variant_ids.barcode_ids',
        string='Barcodes'
    )

    barcode_allow_not_unique = fields.Boolean(
        related='product_variant_ids.barcode_allow_not_unique'
    )
    
