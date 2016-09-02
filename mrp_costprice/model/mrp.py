# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ERP|OPEN (www.erpopen.nl).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime
import openerp.addons.decimal_precision as dp


class mrp_bom(osv.osv):
    _inherit = "mrp.bom"

    def _get_bom_standard_price(self, cr, uid, bom_id, context=None):
        """
        :rtype : float
        """
        if isinstance(bom_id,(long,int)):
            bom_id = [bom_id]

        cost_price = 0.0

        for mainbom in self.browse(cr, uid, bom_id, context=context):
            if mainbom.bom_line_ids:
                cost_price = 0.0
                for line in mainbom.bom_line_ids:
                    cost_price += (line.product_id and line.product_id.standard_price)*(line.product_qty or 0.0) or 0.0
            else:
                cost_price = (mainbom.product_id and mainbom.product_id.standard_price)*\
                                                    (mainbom.product_qty or 0.0) or 0.0
        return cost_price

    def _get_bom_list_price(self, cr, uid, bom_id, context=None):
        """
        :rtype : float
        """
        if isinstance(bom_id,(long,int)):
            bom_id = [bom_id]

        list_price = 0.0

        for mainbom in self.browse(cr, uid, bom_id, context=context):
            if mainbom.bom_line_ids:
                list_price = 0.0
                for line in mainbom.bom_line_ids:
                    list_price += (line.product_id and line.product_id.list_price)*(line.product_qty or 0.0) or 0.0
            else:
                list_price = (mainbom.product_id and mainbom.product_id.list_price)*\
                                                    (mainbom.product_qty or 0.0) or 0.0
        return list_price


    def _get_price(self, cr, uid, ids, field_name, arg, context=None):
        if isinstance(ids,(long, int)):
            ids = [ids]
        if not context:
            context={}
        res={}

        for mainbom in self.browse(cr, uid, ids, context=context):
            res[mainbom.id] = {'bom_cost_price': 0.0, 'bom_base_price': 0.0, 'bom_list_price': 0.0}
            res[mainbom.id]['bom_cost_price'] = self._get_bom_standard_price(cr, uid, mainbom.id, context=context) or 0.0
            res[mainbom.id]['bom_base_price'] = self._get_bom_list_price(cr, uid, mainbom.id, context=context) or 0.0
            if mainbom.list_price_factor:
                res[mainbom.id]['bom_list_price'] = (self._get_bom_list_price(cr, uid, mainbom.id, context=context) or 0.0) * mainbom.list_price_factor
            else:
                res[mainbom.id]['bom_list_price'] = res[mainbom.id]['bom_base_price']
        return res

    def _get_product(self, cr, uid, ids, context=None):

        bom_ids = self.pool.get('mrp.bom').search(cr, uid, [('product_id','in',ids)])

        return bom_ids

    _columns = {
        'bom_cost_price': fields.function(_get_price, string='BOM Cost Price', type='float', readonly=True,
            digits_compute= dp.get_precision('Product Price'), multi='price', store={
                'product.product': (_get_product, ['standard_price','list_price'], 20),
                'mrp.bom': (lambda self, cr, uid, ids, c={}: ids, ['bom_line_ids', 'product_id', 'product_qty'], 20),
                }),
        'bom_base_price': fields.function(_get_price, string='BOM Base Price', type='float', readonly=True,
            digits_compute= dp.get_precision('Product Price'), multi='price', store={
                'product.product': (_get_product, ['standard_price','list_price'], 20),
                'mrp.bom': (lambda self, cr, uid, ids, c={}: ids, ['bom_line_ids', 'product_id', 'product_qty'], 20),
                }),
        'auto_update_costprice': fields.boolean('Automatically update the cost price of the product'),
        'auto_update_listprice': fields.boolean('Automatically update the sale price of the product'),
        'list_price_factor': fields.float('Sale Price Factor'),
        'bom_list_price': fields.function(_get_price, string='BOM Sale Price', type='float', readonly=True,
            digits_compute= dp.get_precision('Product Price'), multi='price', store={
                'product.product': (_get_product, ['standard_price','list_price'], 20),
                'mrp.bom': (lambda self, cr, uid, ids, c={}: ids, ['bom_line_ids', 'product_id', 'product_qty'], 20),
                }),
    }

    _defaults = {
        'auto_update_costprice': lambda *a: 0,
        'auto_update_listprice': lambda *a: 0,
        'list_price_factor': lambda *a: 1,
        }


    def write_cost_price(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        if isinstance(ids,(long, int)):
            ids = [ids]

        for bom in self.browse(cr, uid, ids, context=context):
            # If bom change product cost price
            if bom.bom_line_ids and bom.product_id and bom.auto_update_costprice:
                cost_price = self._get_bom_standard_price(cr, uid, [bom.id],context=context) or 0.0
                product_obj.write(cr, uid, [bom.product_id.id],{'standard_price': cost_price})

    def write_list_price(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product')
        if isinstance(ids,(long, int)):
            ids = [ids]

        for bom in self.browse(cr, uid, ids, context=context):
            # If bom change product list price update
            if bom.bom_line_ids and bom.product_id and bom.auto_update_listprice:
                list_price = self._get_bom_list_price(cr, uid, [bom.id],context=context) or 0.0
                if bom.list_price_factor:
                    list_price = list_price * bom.list_price_factor

                product_obj.write(cr, uid, [bom.product_id.id],{'list_price': list_price})


    # def create(self, cr, uid, vals, context=None):
    #     bom_id = super(mrp_bom, self).create(cr, uid, vals, context=context)
    #     if bom_id:
    #         for bom in self.browse(cr, uid, [bom_id], context=context):
    #             if bom.bom_id:
    #                 self.write_cost_price(cr, uid, [bom.bom_id.id])
    #                 self.write_list_price(cr, uid, [bom.bom_id.id])
    #
    #     return bom_id
    #
    # def write(self, cr, uid, ids, vals, context=None):
    #     return_value = super(mrp_bom, self).write(cr, uid, ids, vals, context=context)
    #     if return_value:
    #         self.write_cost_price(cr, uid, ids, context=context)
    #         self.write_list_price(cr, uid, ids, context=context)
    #
    #     return return_value

class mrp_bom_line(osv.osv):
    _inherit = 'mrp.bom.line'

    _columns = {
        'product_standard_price': fields.related(
            'product_id',
            'standard_price',
            type="float",
            string="Cost Price",
            store=False
        ),

        'product_list_price': fields.related(
            'product_id',
            'list_price',
            type="float",
            string="Sale Price",
            store=False
        )
    }

    def create(self, cr, uid, vals, context=None):
        bom_line_id = super(mrp_bom_line, self).create(
            cr, uid, vals, context=context
        )
        if bom_line_id:
            for bom_line in self.browse(
                    cr, uid, [bom_line_id], context=context
            ):
                if bom_line.bom_id:
                    self.pool.get('mrp.bom').write_cost_price(
                        cr, uid, [bom_line.bom_id.id]
                    )
                    self.pool.get('mrp.bom').write_list_price(
                        cr, uid, [bom_line.bom_id.id]
                    )

        return bom_line_id

    def write(self, cr, uid, ids, vals, context=None):
        return_value = super(mrp_bom_line, self).write(
            cr, uid, ids, vals, context=context
        )
        if return_value:
            for bom_line in self.browse(cr, uid, ids, context=context):
                if bom_line.bom_id:
                    self.pool.get('mrp.bom').write_cost_price(
                        cr, uid, [bom_line.bom_id.id]
                    )
                    self.pool.get('mrp.bom').write_list_price(
                        cr, uid, [bom_line.bom_id.id]
                    )

        return return_value


class product_product(osv.osv):
    _inherit = "product.product"

    def write(self, cr, uid, ids, vals, context=None):

        return_value = super(product_product, self).write(cr, uid, ids, vals, context=context)
        bom_pool = self.pool.get('mrp.bom')
        bom_line_pool = self.pool.get('mrp.bom.line')

        if isinstance(ids,(long, int)):
            ids = [ids]

        for product in self.browse(cr, uid, ids, context=context):

            bom_line_ids = bom_line_pool.search(cr, uid, [('product_id','=',product.id)])

            if isinstance(bom_line_ids, (long,int)):
                bom_line_ids = [bom_line_ids]

            for line in bom_line_pool.browse(cr, uid, bom_line_ids, context=context):
                if line.bom_id.product_id and line.bom_id.auto_update_costprice:
                    # update cost price
                    standard_price = bom_pool._get_bom_standard_price(cr, uid, line.bom_id.id, context=context) or 0.0
                    self.write(cr, uid, line.bom_id.product_id.id,{'standard_price': standard_price})

                if line.bom_id.product_id and line.bom_id.auto_update_listprice:
                    # update list price
                    list_price = bom_pool._get_bom_list_price(cr, uid, line.bom_id.id, context=context) or 0.0
                    if line.bom_id.list_price_factor:
                        list_price = list_price * line.bom_id.list_price_factor
                    self.write(cr, uid, line.bom_id.product_id.id,{'list_price': list_price})

        return return_value
