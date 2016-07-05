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

class product_pricelist(models.Model):
    _inherit = 'product.pricelist'
    
    show_on_products = fields.Boolean(string="Display on product page")
    product_price = fields.Float(
            compute="_get_product_price",
            inverse="_set_product_price",
            string="Price"
    )
    product_id = fields.Integer(
            #comodel_name="product.product",
            compute="_get_product_price",
            string="product_id"
    )

    @api.one
    def _get_product_price(self):
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

        self.product_price = self.price_get(
                product_id, 1).get(self.id, 0.0
                                   )
        self.product_id = product_id

    def _set_product_price(self):
            # Real change takes place in price_set after inverse
            # method of pricelists object on product_template
            _logger.debug("Set Price: %s", self.product_price)

    def price_set(self, product_template, new_price):
        """
        Set the price of the product in current pricelist
        if different from price through  pricerules
        :param product_template: product_template object
        :param new_price: new price
        :return:
        """
        if new_price:

            version = self.get_active_pricelist_version()
            if not version:
                return False
            items = self.env['product.pricelist.item'].search(
                    [
                        ('product_tmpl_id','=', product_template.id),
                        ('price_version_id', '=', version.id)
                    ]
            )
            product_price_type_ids = self.env['product.price.type'].search(
                    [
                        ('field', '=', 'list_price')
                    ]
            )
            if not items:
                self.env['product.pricelist.item'].create(
                        {
                            'base': product_price_type_ids and product_price_type_ids[0].id,
                            'sequence': 1,
                            'name': product_template.name,
                            'product_tmpl_id': product_template.id,
                            'price_version_id': version.id,
                            'price_surcharge': new_price,
                            'price_discount': -1
                        }
                )
            else:
                for item in items:
                    item.write(
                            {
                                'base': product_price_type_ids and product_price_type_ids[0].id,
                                'sequence': 1,
                                'name': product_template.name,
                                'product_id': product_template.id,
                                'price_version_id': version.id,
                                'price_surcharge': new_price,
                                'price_discount': -1
                            }
                    )
            return True


    def get_active_pricelist_version(self):
        date = self.env.context.get('date') or fields.Date.context_today(self)

        version = False
        for v in self.version_id:
            if ((v.date_start is False) or (v.date_start <= date)) and ((v.date_end is False) or (v.date_end >= date)):
                version = v
                break

        return version