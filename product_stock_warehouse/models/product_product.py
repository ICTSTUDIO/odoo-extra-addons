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

class ProductProduct(models.Model):
    _inherit = 'product.product'

    warehouses = fields.One2many(
            comodel_name="stock.warehouse",
            string="Warehouse Stock",
            compute="_get_stock",
            inverse="_set_stock"
    )

    @api.one
    def _get_stock(self):
        self.warehouses = self.env['stock.warehouse'].search(
                [
                    ('show_on_products', '=', True)
                ]
        )

    @api.one
    def _set_stock(self):

        for warehouse in self.warehouses:
            _logger.debug("Warehouse: %s", warehouse)
            if warehouse.product_qty_available:
                _logger.debug("PP Set Stock: Warehouse: %s", warehouse.name)
                _logger.debug("PP Set Stock: Warehouse Stock: %s", warehouse.product_qty_available)
                warehouse.stock_set(self, warehouse.product_qty_available)