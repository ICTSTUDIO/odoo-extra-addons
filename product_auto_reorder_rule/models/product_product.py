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
    _inherit = 'product.product'

    @api.multi
    def create_reorder_rule(self, min_qty=0.0, max_qty=0.0, qty_multiple=1.0, overwrite=False):
        swo_obj = self.env['stock.warehouse.orderpoint']
        for rec in self:
            reorder_rules = swo_obj.search([('product_id', '=', rec.id)])
            reorder_vals = {
                'product_id': rec.id,
                'product_min_qty': min_qty,
                'product_max_qty': max_qty,
                'qty_multiple': qty_multiple,
                'active': True,
                'product_uom': rec.uom_id.id,
            }

            if rec.type in ('product', 'consu') and not reorder_rules:
                self.env['stock.warehouse.orderpoint'].create(reorder_vals)
            elif rec.type in ('product', 'consu') and reorder_rules and overwrite:
                for reorder_rule in reorder_rules:
                    reorder_rule.write(reorder_vals)

    @api.model
    def create(self, vals):

        return_create = super(ProductProduct, self).create(vals)

        if return_create:
            return_create.create_reorder_rule()

            return return_create

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        self.create_reorder_rule()
        return res