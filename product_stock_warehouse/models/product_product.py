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
from openerp.tools.safe_eval import safe_eval as eval
import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round
from openerp.exceptions import except_orm

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    qty_available = fields.Float(
            compute="_new_product_available",
            search="_search_product_qty_available",
            digits_compute=dp.get_precision('Product Unit of Measure')
    )
    virtual_available = fields.Float(
            compute="_new_product_available",
            search="_search_product_virtual_available",
            digits_compute=dp.get_precision('Product Unit of Measure')
    )
    incoming_qty = fields.Float(
            compute="_new_product_available",
            search="_search_product_incoming_qty",
            digits_compute=dp.get_precision('Product Unit of Measure')
    )
    outgoing_qty = fields.Float(
            compute="_new_product_available",
            search="_search_product_outgoing_qty",
            digits_compute=dp.get_precision('Product Unit of Measure')
    )

    warehouses = fields.One2many(
            comodel_name="stock.warehouse",
            string="Warehouse Stock",
            compute="_get_stock",
            inverse="_set_stock"
    )

    @api.multi
    def _new_product_available(self):

        domain_products = [('product_id', 'in', self.ids)]
        domain_quant, domain_move_in, domain_move_out = [], [], []
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
        domain_move_in += self._get_domain_dates() + [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_products
        domain_move_out += self._get_domain_dates() + [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_products
        domain_quant += domain_products

        if self._context.get('lot_id'):
            domain_quant.append(('lot_id', '=', self._context['lot_id']))
        if self._context.get('owner_id'):
            domain_quant.append(('owner_id', '=', self._context['owner_id']))
            owner_domain = ('restrict_partner_id', '=', self._context['owner_id'])
            domain_move_in.append(owner_domain)
            domain_move_out.append(owner_domain)
        if self._context.get('package_id'):
            domain_quant.append(('package_id', '=', self._context['package_id']))

        domain_move_in += domain_move_in_loc
        domain_move_out += domain_move_out_loc
        moves_in = self.pool.get('stock.move').read_group(self._cr, self._uid, domain_move_in, ['product_id', 'product_qty'], ['product_id'], context=self._context)
        moves_out = self.pool.get('stock.move').read_group(self._cr, self._uid, domain_move_out, ['product_id', 'product_qty'], ['product_id'], context=self._context)

        domain_quant += domain_quant_loc
        quants = self.pool.get('stock.quant').read_group(self._cr, self._uid, domain_quant, ['product_id', 'qty'], ['product_id'], context=self._context)
        quants = dict(map(lambda x: (x['product_id'][0], x['qty']), quants))

        moves_in = dict(map(lambda x: (x['product_id'][0], x['product_qty']), moves_in))
        moves_out = dict(map(lambda x: (x['product_id'][0], x['product_qty']), moves_out))

        for product in self:
            id = product.id
            qty_available = float_round(quants.get(id, 0.0), precision_rounding=product.uom_id.rounding)
            incoming_qty = float_round(moves_in.get(id, 0.0), precision_rounding=product.uom_id.rounding)
            outgoing_qty = float_round(moves_out.get(id, 0.0), precision_rounding=product.uom_id.rounding)
            virtual_available = float_round(quants.get(id, 0.0) + moves_in.get(id, 0.0) - moves_out.get(id, 0.0), precision_rounding=product.uom_id.rounding)

            product.qty_available = qty_available or 0.0
            product.incoming_qty = incoming_qty or 0.0
            product.outgoing_qty = outgoing_qty or 0.0
            product.virtual_available = virtual_available or 0.0

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


    def _search_product_qty_available(self, operator, value):
        res = self._search_product_filter_quantity(operator, value, 'qty_available')
        return res

    def _search_product_virtual_available(self, operator, value):
        res = self._search_product_filter_quantity(operator, value, 'virtual_available')
        return res

    def _search_product_incoming_qty(self, operator, value):
        res = self._search_product_filter_quantity(operator, value, 'incoming_qty')
        return res


    def _search_product_outgoing_qty(self, operator, value):
        res = self._search_product_filter_quantity(operator, value, 'outgoing_qty')
        return res

    def _get_qty_filter_fields(self):
        return  ['qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty']

    def _search_product_filter_quantity(self, operator, value, filter_field):
        res = []
        ids = []
        assert filter_field in self._get_qty_filter_fields(), 'Invalid domain left operand'
        assert operator in ('<', '>', '=', '!=', '<=', '>='), 'Invalid domain operator'
        assert isinstance(value, (float, int)), 'Invalid domain right operand'
        if operator == '=':
            operator = '=='

        if filter_field == 'qty_available' and (value != 0.0 or operator not in  ('==', '>=', '<=')):
            res.append(('id', 'in', self._search_product_filter_qty_available(operator, value)))
        else:
            products = self.search([])

            if products:
            #TODO: Still optimization possible when searching virtual quantities
                for element in products:
                    if eval(str(element[filter_field]) + operator + str(value)):
                        ids.append(element.id)
            res.append(('id', 'in', ids))
        return res

    def _search_product_filter_qty_available(self, operator, value):
        domain_quant = []
        if self._context.get('lot_id'):
            domain_quant.append(('lot_id', '=', self._context['lot_id']))
        if self._context.get('owner_id'):
            domain_quant.append(('owner_id', '=', self._context['owner_id']))
        if self._context.get('package_id'):
            domain_quant.append(('package_id', '=', self._context['package_id']))
        domain_quant += self._get_domain_locations()[0]
        quants = self.pool.get('stock.quant').read_group(self._cr, self._uid, domain_quant, ['product_id', 'qty'], ['product_id'], context=self._context)
        quants = dict(map(lambda x: (x['product_id'][0], x['qty']), quants))
        quants = dict((k, v) for k, v in quants.iteritems() if eval(str(v) + operator + str(value)))
        return(list(quants))