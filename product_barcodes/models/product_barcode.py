# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ERP|OPEN (www.erpopen.nl).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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

    #@api.one
    #@api.constrains('name')
    #def _check_name_digits(self):
    #    if not self.name.isnumeric():
    #        raise ValidationError("The following barcode is invalid: %s. Barcodes can only have numbers" % self.name)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Barcode needs to be unique'),
    ]