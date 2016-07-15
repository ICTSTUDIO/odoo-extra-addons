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
            comodel_name="stock.warehouse",
            string="Locations",
            compute="_get_locations",
            inverse="_set_locations"
    )

    product_location = fields.Char(
            string="Current Location",
            compute="_get_product_location",

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

        if not warehouse_id:
            warehouse_id = self._get_default_warehouse()

        if warehouse_id:
            warehouse_location = self.env['product.stock.location'].search(
                [
                    ('warehouse_id', '=', warehouse_id),
                    ('product_id', '=', self.id)

                ]
            )

            if warehouse_location and warehouse_location[0]:
                self.product_location = warehouse_location[0].location


    @api.one
    def _get_locations(self):
        self.locations = self.env['stock.warehouse'].search(
                [
                    ('show_location_on_products', '=', True)
                ]
        )

    @api.one
    def _set_locations(self):
        for location in self.locations:

            _logger.debug("location: %s", location)
            _logger.debug("location: %s", self)
            _logger.debug("location: %s", location.product_location)
            # if location.product_location:
            #         location.location_set(self, location.product_location)