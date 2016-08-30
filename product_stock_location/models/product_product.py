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

    locations = fields.One2many(
            comodel_name="product.stock.location",
            inverse_name="product_id",
            string="Locations",
    )

    product_location = fields.Char(
            string="Location",
            compute="_get_product_location",
            search="_search_product_location"
    )

    @api.model
    def _get_default_warehouse(self):
        if 'default_operating_unit_id' in self.env.user._fields:
            warehouse_id = self.env.user.default_operating_unit_id.sale_warehouse.id
        else:
            warehouse = self.env['stock.warehouse'].search([])[0]
            warehouse_id = warehouse.id
        return warehouse_id

    @api.one
    def _get_product_location(self):
        warehouse_id = False
        if self.env.context.get('warehouse'):
            warehouse_id = self.env.context.get('warehouse')
        if self.env.context.get('warehouse_id'):
            warehouse_id = self.env.context.get('warehouse_id')

        location_id = False
        if self.env.context.get('location_id'):
            location_id = self.env.context.get('location_id')

        self.product_location = '-'
        if not warehouse_id:
            warehouse_id = self._get_default_warehouse()

        if warehouse_id:
            location = self.locations.filtered(lambda r: r.warehouse_id.id == warehouse_id)

            if location and location[0] and location[0].location:
                self.product_location = location[0].location

        if location_id:
            location = self.locations.filtered(lambda r: r.warehouse_location_id.id == location_id)

            if location and location[0] and location[0].location:
                self.product_location = location[0].location

    def _search_product_location(self, operator, value):
        locations = self.env['product.stock.location']._search_locations(operator, value)
        _logger.debug("Products: %s", locations)
        _logger.debug("ProductsIDS: %s", locations.ids)
        return [('locations', 'in', locations.ids)]