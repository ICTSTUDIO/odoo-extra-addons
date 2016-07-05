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
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    _order = 'name'
    
    show_on_products = fields.Boolean(string="Display on product page")

    orderpoint_qty_multiple = fields.Float(
            compute="_get_product_orderpoint",
            string="Quantity Multiple",
            digits=dp.get_precision('Product Unit of Measure')
    )

    orderpoint_min_qty = fields.Float(
            compute="_get_product_orderpoint",
            string="Minimum Quantity",
            digits=dp.get_precision('Product Unit of Measure')
    )

    product_incoming = fields.Float(
            compute="_get_product_stock",
            string="Incoming Products",
            digits=dp.get_precision('Product Unit of Measure')

    )
    product_transit = fields.Float(
            compute="_get_product_stock",
            string="Products in Transit",
            digits=dp.get_precision('Product Unit of Measure')

    )
    product_outgoing = fields.Float(
            compute="_get_product_stock",
            string="Outgoing Products",
            digits=dp.get_precision('Product Unit of Measure')
    )

    product_virtual_available = fields.Float(
            compute="_get_product_stock",
            string="Virtual Available",
            digits=dp.get_precision('Product Unit of Measure')
    )

    product_free_available = fields.Float(
            compute="_get_product_stock",
            string="Free Available",
            digits=dp.get_precision('Product Unit of Measure')
    )
    product_backorder = fields.Float(
            compute="_get_product_stock",
            string="Backorder",
            digits=dp.get_precision('Product Unit of Measure')
    )

    product_qty_available = fields.Float(
            compute="_get_product_stock",
            #inverse="_set_product_stock",
            string="Qty On Hand",
            digits=dp.get_precision('Product Unit of Measure')
    )
    product_id = fields.Integer(
            #comodel_name="product.product",
            compute="_get_product_stock",
            string="product_id"
    )

    @api.one
    def _get_product_stock(self):
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


        product = self.env['product.product'].with_context(location=self.lot_stock_id.id).browse(product_id)
        self.product_qty_available = product.qty_available
        self.product_free_available = product.qty_available-product.outgoing_qty
        self.product_virtual_available = product.virtual_available
        self.product_incoming = product.incoming_qty
        self.product_outgoing = product.outgoing_qty
        if product.qty_available+product.outgoing_qty < 0:
            self.product_backorder = product.qty_available+product.outgoing_qty
        else:
            self.product_backorder = 0

        transit_locations = self.env['stock.location'].search([('usage', '=', 'transit')])
        self.product_transit = 0
        for transit_location in transit_locations:
            warehouse = transit_location.get_warehouse(transit_location)
            if warehouse and warehouse == self.id:
                product = self.env['product.product'].with_context(location=transit_location.id).browse(product_id)
                self.product_transit = product.qty_available

        self.product_id = product_id

    @api.one
    def _set_product_stock(self):
        # Real change initiated on product_template and product_product
        _logger.debug("Set Product Stock")

    @api.one
    def _get_product_orderpoint(self):
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

        self.product_id = product_id

        orderpoints = self.env['stock.warehouse.orderpoint'].search(
                [
                    ('product_id', '=', product_id),
                    ('warehouse_id', '=', self.id)
                ]
        )
        if orderpoints and orderpoints[0]:
            self.orderpoint_min_qty = orderpoints[0].product_min_qty
            self.orderpoint_qty_multiple = orderpoints[0].qty_multiple

    @api.model
    def stock_set(self, product, new_qty):
        _logger.debug("Set Stock Set")

        inventory_obj = self.env['stock.inventory']
        inventory_line_obj = self.env['stock.inventory.line']

        inventory = inventory_obj.create(
                {
                    'name': _('INV: %s') % (product.name),
                'filter': 'product',
                'product_id': product.id,
                'location_id': self.lot_stock_id.id,
                }
        )

        th_qty = product.with_context(location=self.lot_stock_id.id).qty_available
        line_data = {
            'inventory_id': inventory.id,
            'product_qty': new_qty,
            'location_id': self.lot_stock_id.id,
            'product_id': product.id,
            'product_uom_id': product.uom_id.id,
            'theoretical_qty': th_qty,
        }
        inventory_line_obj.create(line_data)
        inventory.action_done()

    @api.multi
    def open_related_moves(self):
        """ Open the Related Stock Moves
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        _logger.debug("Product_id: %s", self.product_id)
        ctx = dict(
                search_default_product_id=self.product_id,
                search_default_location_id=self.lot_stock_id.id
        )

        return {
            'name': _('Open Related Stock Moves'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.move.location',
            'src_model': 'stock.warehouse',
            # 'views': [(compose_form.id, 'form')],
            # 'view_id': compose_form.id,
            'target': 'current',
            'context': ctx,
        }

    @api.multi
    def change_product_quantity(self):
        """ Change Stock
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        _logger.debug("Product_id: %s", self.product_id)
        ctx = dict(
                warehouse_product_id=self.product_id,
                warehouse_location_id=self.lot_stock_id.id,
                warehouse_product_qty=self.product_qty_available or 1
        )

        return {
            'name': _('Change Product Qty'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'warehouse.change.product.qty',
            'src_model': 'stock.warehouse',
            # 'views': [(compose_form.id, 'form')],
            # 'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }