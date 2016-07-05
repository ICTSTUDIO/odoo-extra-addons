# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
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

from openerp import models, fields, api

class ProductCreateReorderRule(models.TransientModel):
    _name = 'product.create.reorder.rule'

    overwrite = fields.Boolean(
            string='Overwrite Existing Orderpoints',
            default=False
    )
    min_qty = fields.Float(
            string='Min Qty',
            default=0.0,
            required=True
    )
    max_qty = fields.Float(
            string='Max Qty',
            default=0.0,
            required=True
    )
    qty_multiple = fields.Float(
            string='Qty Multiple',
            default=1.0,
            required=True
    )

    @api.multi
    def create_rules(self):
        product_obj = self.env['product.product']
        for product_id in self.env.context.get('active_ids', []):
            product = product_obj.browse(product_id)
            product.create_reorder_rule(
                min_qty=self.min_qty,
                max_qty=self.max_qty,
                qty_multiple=self.qty_multiple,
                overwrite=self.overwrite
            )