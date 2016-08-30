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
import logging

from openerp.osv import orm, fields

_logger = logging.getLogger(__name__)


class ProductProduct(orm.Model):
    _inherit = 'product.product'

    # disable constraint
    def _check_ean_key(self, cr, uid, ids):
        "Inherit the method to disable the EAN13 check"
        return True
    _constraints = [(_check_ean_key, 'Error: Invalid ean code', ['ean13'])]

    # def search(self, cr, uid, args, offset=0, limit=None,
    #            order=None, context=None, count=False):
    #     """overwrite the search method in order to search
    #     on all ean13 codes of a product when we search an ean13"""
    #
    #     if filter(lambda x: x[0] == 'ean13', args):
    #         # get the operator of the search
    #         ean_operator = filter(lambda x: x[0] == 'ean13', args)[0][1]
    #         # get the value of the search
    #         ean_value = filter(lambda x: x[0] == 'ean13', args)[0][2]
    #         # search the ean13
    #         barcode_ids = self.pool.get('product.barcode').search(
    #             cr, uid, [('name', ean_operator, ean_value)])
    #
    #         # get the other arguments of the search
    #         args = filter(lambda x: x[0] != 'ean13', args)
    #         # add the new criterion
    #         args += [('barcode_ids', 'in', barcode_ids)]
    #
    #     return super(ProductProduct, self).search(
    #         cr, uid, args, offset, limit, order, context=context, count=count)