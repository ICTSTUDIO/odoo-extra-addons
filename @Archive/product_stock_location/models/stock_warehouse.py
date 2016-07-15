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

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    show_location_on_products = fields.Boolean(string="Display Location on product page")

    product_location = fields.Char(
            compute="_get_product_location",
            inverse="_set_product_location",
            string="Location"
    )

    product_id = fields.Integer(
            #comodel_name="product.product",
            compute="_get_product_location",
            string="product_id"
    )

    @api.multi
    def _set_product_location(self):
        """ Wrapper to do nothing """
        _logger.debug(self.product_id)
        product = self.env['product.product'].browse(self.product_id)
        _logger.debug('Product: %s', product)
        _logger.debug("Not used")
        _logger.debug("self: %s", self)
        _logger.debug("location: %s", self.product_location)
        if not self.product_location:
            new_location = '-'
        else:
            new_location = self.product_location
            _logger.debug("New Location")
        _logger.debug("Context: %s", self._context)
        update_location = {'warehouse_id': self.id, 'location': self.product_location}
        if self._context.get('updated_locations'):
            changed_locations = self._context.get('updated_locations')
        else:
            changed_locations = []
        changed_locations.append(update_location)
        ctx = dict(self._context, updated_locations=changed_locations)
        super(self.with_context(ctx))._set_product_location()

    @api.one
    def _get_product_location(self):
        if self.env.context.get('product_template_id', False):
            product_tmpl = self.env['product.template'].browse(
                    [self.env.context.get('product_template_id')]
            )
            product_id = False
            if product_tmpl:
                product_tmpl_id = product_tmpl[0]
                if product_tmpl_id and product_tmpl_id.product_variant_ids:
                    product = product_tmpl_id.product_variant_ids[0]
                    if product:
                        product_id = product.id
            if not product_id:
                return False

        elif self.env.context.get('product_id', False):
            product_id = self.env.context.get('product_id')
        else: 
            return False

        product = self.env['product.stock.location'].search(
                [
                    ('product_id','=', product_id),
                    ('warehouse_id','=', self.id)
                ]
        )
        if product and product[0]:
            self.product_location = product[0].location
        else:
            self.product_location = '-'

    @api.model
    def location_set(self, product, new_location):
        """
        Set the location of the product in current warehouse
        :param product_product: product_product object
        :param new_location: new location
        :return:
        """
        if new_location:
            locations = self.env['product.stock.location'].search(
                    [
                        ('product_id','=', product.id),
                        ('warehouse_id', '=', self.id),
                    ]
            )
            if not locations:
                self.env['product.stock.location'].create(
                        {
                            'product_id': product.id,
                            'warehouse_id': self.id,
                            'location': new_location,
                        }
                )
            else:
                for location in locations:
                    location.write(
                            {
                                'product_id': product.id,
                                'warehouse_id': self.id,
                                'location': new_location,
                            }
                    )
            return True
