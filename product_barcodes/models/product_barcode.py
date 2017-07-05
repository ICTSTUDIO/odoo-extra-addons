# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright© 2015-2017 ERP|OPEN <http://www.erpopen.nl>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ProductBarcode(models.Model):
    _name = 'product.barcode'
    _description = "List of barcodes for a product."

    name = fields.Char(string="Barcode")
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product"
    )

    @api.one
    @api.constrains('name')
    def _check_name_length(self):
        if len(self.name) < 4:
            raise ValidationError("The following barcode is invalid: %s. Barcodes needs to be larger than 3 numbers" % self.name)

    @api.one
    @api.constrains('name', 'product_id')
    def _check_duplicate_name(self):
        if not self.product_id.barcode_allow_not_unique:
            found_barcodes = self.search([('name', '=', self.name)])
            if len(found_barcodes) > 1:
                raise ValidationError("The following barcode is not unique: %s. Barcode is used with the following products: %s" % (self.name, found_barcodes.ids))

    _sql_constraints = [
        ('name_uniq', 'unique(name, product_id)', 'Barcode needs to be unique'),
    ]