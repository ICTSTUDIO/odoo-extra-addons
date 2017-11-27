# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    @api.depends('barcode_ids.name')
    def get_barcodes(self):
        for rec in self:
            rec.ean13 = rec._get_barcodes()

    @api.multi
    def _get_barcodes(self):
        return ', '.join([bc.name for bc in self.barcode_ids])

    barcode_ids = fields.One2many(
        comodel_name="product.barcode",
        inverse_name="product_id",
        string='Barcodes'
    )
    ean13 = fields.Char(
            compute="get_barcodes",
            string="Barcodes",
            size=200,
            readonly=True,
            store=True
    )
    barcode_allow_not_unique = fields.Boolean(string="Allow barcode not unique", default=False)

