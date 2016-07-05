# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    stock_product_location_ids = fields.One2many(
            comodel_name='stock_product_location',
            inverse_name='product_id',
            string='Location Stock '
    )

    stock_product_warehouse_ids = fields.One2many(
            comodel_name='stock_product_warehouse',
            inverse_name='product_id',
            string='Warehouse Stock '
    )

    @api.one
    def copy(self, default=None):
        default = dict(default or {})

        default['stock_product_location_ids'] = []
        default['stock_product_warehouse_ids'] = []

        return super(ProductProduct, self).copy(default)