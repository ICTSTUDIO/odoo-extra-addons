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

from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductStockLocation(models.Model):
    _name = 'product.stock.location'

    warehouse_id = fields.Many2one(
            comodel_name="stock.warehouse",
            string="Warehouse"
    )
    product_id = fields.Many2one(
            comodel_name="product.product",
            string="Product"
    )
    location = fields.Char(
            string="Location"
    )
    warehouse_location_id = fields.Many2one(
            comodel_name="stock.location",
            related='warehouse_id.lot_stock_id'
    )

    def _search_locations(self, operator, value):
        return self.search([('location',operator, value)])
