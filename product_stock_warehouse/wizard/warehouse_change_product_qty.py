# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


_logger = logging.getLogger(__name__)

class WarehouseChangeProductQty(models.TransientModel):
    _name = 'warehouse.change.product.qty'

    product_id = fields.Many2one(
            comodel_name='product.product',
            string='Product',
            default=lambda self: self._context.get('warehouse_product_id')
    )
    new_quantity = fields.Float(
            string='New Quantity on Hand',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            required=True,
            help='This quantity is expressed in the Default Unit of Measure of the product.',
            default=lambda self: self._context.get('warehouse_product_qty')
    )
    location_id = fields.Many2one(
            comodel_name='stock.location',
            string='Location',
            required=True,
            domain="[('usage', '=', 'internal')]",
            default=lambda self: self._context.get('warehouse_location_id')
    )

    # def default_get(self, cr, uid, fields, context):
    #     """ To get default values for the object.
    #      @param self: The object pointer.
    #      @param cr: A database cursor
    #      @param uid: ID of the user currently logged in
    #      @param fields: List of fields for which we want default values
    #      @param context: A standard dictionary
    #      @return: A dictionary which of fields with values.
    #     """
    #
    #     res = super(stock_change_product_qty, self).default_get(cr, uid, fields, context=context)
    #
    #     if context.get('active_model') == 'product.template':
    #         product_ids = self.pool.get('product.product').search(cr, uid, [('product_tmpl_id', '=', context.get('active_id'))], context=context)
    #         if len(product_ids) == 1:
    #             res['product_id'] = product_ids[0]
    #         else:
    #             raise orm.except_orm(_('Warning'), _('Please use the Product Variant view to update the product quantity.'))
    #
    #     if 'location_id' in fields:
    #         location_id = res.get('location_id', False)
    #         if not location_id:
    #             try:
    #                 model, location_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'stock_location_stock')
    #             except (orm.except_orm, ValueError):
    #                 pass
    #         if location_id:
    #             try:
    #                 self.pool.get('stock.location').check_access_rule(cr, uid, [location_id], 'read', context=context)
    #             except (orm.except_orm, ValueError):
    #                 location_id = False
    #         res['location_id'] = location_id
    #     return res

    @api.one
    def set_quantity(self):
        _logger.debug("Set Stock Set")

        inventory_obj = self.env['stock.inventory']
        inventory_line_obj = self.env['stock.inventory.line']

        inventory = inventory_obj.create(
                {
                    'name': _('INV: %s') % (self.product_id.name),
                    'filter': 'product',
                    'product_id': self.product_id.id,
                    'location_id': self.location_id.id,
                }
        )

        th_qty = self.env['product.product'].with_context(location=self.location_id.id).qty_available
        line_data = {
            'inventory_id': inventory.id,
            'product_qty': self.new_quantity or 0,
            'location_id': self.location_id.id,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'theoretical_qty': th_qty,
        }
        _logger.debug('Inv line: %s', line_data)

        inventory_line_obj.create(line_data)
        inventory.action_done()

        return True
