# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import math

from openerp import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class StockWarehouseTransferProduct(models.TransientModel):
    _name = 'stock.warehouse.transfer.product'
    _description = 'Stock Warehouse Transfer Product'

    source_warehouse = fields.Many2one(
            comodel_name='stock.warehouse',
            string='Source Warehouse')
    dest_warehouse = fields.Many2one(
            comodel_name='stock.warehouse',
            string='Destination Warehouse')
    transfer_type = fields.Selection(
            selection=[('min_qty', 'Fill to the minimum quantity')],
            string='Transfer Type',
            default=lambda self: self._default_transfer_type()
    )
    product_ids = fields.Many2many(
            comodel_name='product.product',
            relation='rel_transfer_products',
            column1='transfer_product_id',
            column2='product_id',
            string='Products'
    )
    location_id = fields.Many2one(
            related='dest_warehouse.lot_stock_id'
    )

    @api.model
    def _default_transfer_type(self):
        return 'min_qty'

    @api.model
    def _calc_product_qty(self, min_qty, qty_multiple, qty_available):
        if min_qty > qty_available and min_qty != 0:
            return math.ceil((min_qty - qty_available) / qty_multiple) * qty_multiple
        return 0

    @api.model
    def get_product_qty(self, product):
        if self.transfer_type == 'min_qty':
            ctx = dict(self._context, location_id=self.dest_warehouse.lot_stock_id.id, location=self.dest_warehouse.lot_stock_id.id)
            other_product = product.with_context(ctx)

            min_qty = other_product.orderpoint_min_qty
            qty_multiple = other_product.orderpoint_qty_multiple
            qty_available = other_product.qty_available

            return self._calc_product_qty(min_qty, qty_multiple, qty_available)
        else:
            return 0

    @api.model
    def create_transfer_lines(self, transfer):
        for product in self.product_ids:
            transfer_line = self.env['stock.warehouse.transfer.line']
            product_qty = self.get_product_qty(product)
            if product_qty:
                transfer_line.create(
                        {
                            'product_id': product.id,
                            'product_uom_id': product.uom_id and product.uom_id.id,
                            'product_qty': product_qty,
                            'transfer': transfer.id
                        }
                )

    @api.multi
    def create_transfer(self):
        transfer = self.env['stock.warehouse.transfer'].create(
                {
                    'source_warehouse': self.source_warehouse.id,
                    'dest_warehouse': self.dest_warehouse.id
                }
        )
        if transfer:
            self.create_transfer_lines(transfer)



            return {
                #'domain': "[('id','=',%d)]" % (transfer.id),
                'name': _('Warehouse Transfer'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'stock.warehouse.transfer',
                'res_id': transfer.id,
                'view_id': False,
                'type': 'ir.actions.act_window'
            }