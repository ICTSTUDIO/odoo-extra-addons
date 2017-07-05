# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright© 2015-2017 ERP|OPEN <http://www.erpopen.nl>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.one
    @api.depends('barcode_ids.name')
    def _get_barcodes(self):
        barcode_list=[]
        for barcode in self.barcode_ids:
            barcode_list.append(barcode.name)

        self.ean13=str(barcode_list)

    barcode_ids = fields.One2many(
        comodel_name="product.barcode",
        inverse_name="product_id",
        string='Barcodes'
    )
    ean13 = fields.Char(
            compute="_get_barcodes",
            string="Barcodes",
            size=200,
            readonly=True,
            store=True
    )
    barcode_allow_not_unique = fields.Boolean(string="Allow barcode not unique", default=False)

    @api.one
    @api.depends('barcode_ids.name')
    def _get_barcodes(self):
        barcode_list=''
        for barcode in self.barcode_ids:
            if not barcode_list:
                barcode_list = barcode.name
            else:
                barcode_list += ', ' + barcode.name

        self.ean13=str(barcode_list)