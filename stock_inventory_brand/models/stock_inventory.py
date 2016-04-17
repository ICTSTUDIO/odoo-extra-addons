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

class StockInventory(models.Model):
    _inherit = "stock.inventory"

    product_brand_id = fields.Many2one(
            comodel_name='product.brand',
            string='Inventoried Brand',
            readonly=True,
            states={'draft': [('readonly', False)]},
            help="Specify Product Brand to focus your inventory on a particular Brand."
    )

    filter = fields.Selection(
            selection='_get_available_filters'
    )

    @api.model
    def _get_available_filters(self):
        res_filter = super(StockInventory, self)._get_available_filters()
        res_filter.append(('brand', _('Only Products from Brand')))
        return res_filter

    @api.model
    def _get_inventory_lines(self, inventory):
        if inventory.product_brand_id:
            location_obj = self.env['stock.location']
            product_obj = self.env['product.product']
            locations = location_obj.search(
                    [
                        ('id', 'child_of', [inventory.location_id.id])
                    ]
            )

            domain = ' sq.location_id in %s'
            args = (tuple(locations.ids),)
            if inventory.partner_id:
                domain += ' and sq.owner_id = %s'
                args += (inventory.partner_id.id,)
            if inventory.lot_id:
                domain += ' and sq.lot_id = %s'
                args += (inventory.lot_id.id,)
            if inventory.product_id:
                domain += ' and sq.product_id = %s'
                args += (inventory.product_id.id,)
            if inventory.package_id:
                domain += ' and sq.package_id = %s'
                args += (inventory.package_id.id,)
            if inventory.product_brand_id:
                domain += ' and pt.product_brand_id = %s'
                args += (inventory.product_brand_id.id,)

            self.env.cr.execute('''
                   SELECT sq.product_id as product_id, sum(sq.qty) as product_qty, sq.location_id as location_id,
                   sq.lot_id as prod_lot_id, sq.package_id as package_id, sq.owner_id as partner_id, pt.product_brand_id as product_brand_id
                   FROM stock_quant as sq
                   INNER JOIN product_product as pp on pp.id =  sq.product_id
                   INNER JOIN product_template as pt on pp.product_tmpl_id = pt.id
                   WHERE''' + domain + '''
                   GROUP BY sq.product_id, sq.location_id, sq.lot_id, sq.package_id, sq.owner_id, pt.product_brand_id
                ''', args)
            vals = []
            for product_line in self.env.cr.dictfetchall():
                #replace the None the dictionary by False, because falsy values are tested later on
                for key, value in product_line.items():
                    if not value:
                        product_line[key] = False
                product_line['inventory_id'] = inventory.id
                product_line['theoretical_qty'] = product_line['product_qty']
                if product_line['product_id']:
                    product = product_obj.browse(product_line['product_id'])
                    product_line['product_uom_id'] = product.uom_id.id
                vals.append(product_line)
        else:
            vals = super(StockInventory, self)._get_inventory_lines(inventory)
        return vals
