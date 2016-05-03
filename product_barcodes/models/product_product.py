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