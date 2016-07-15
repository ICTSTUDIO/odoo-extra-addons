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

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class StockWarehouseTransferLine(models.Model):
    _name = 'stock.warehouse.transfer.line'
    _rec_name = 'product_id'


    @api.model
    def _get_default_product_qty(self):
        return 1.0


    product_id = fields.Many2one(
            comodel_name='product.product',
            string='Product')
    product_qty = fields.Float(
            string='Quantity',
            default=_get_default_product_qty)
    product_uom_id = fields.Many2one(
            comodel_name='product.uom',
            string='Unit of Measure')
    transfer = fields.Many2one(
            comodel_name='stock.warehouse.transfer',
            string='Transfer')
    note = fields.Text(string='Note')
    source_location = fields.Many2one(
            comodel_name='stock.location',
            string='Source Location',
            compute='_get_transfer_locations',
            store=True)
    dest_location = fields.Many2one(
            comodel_name='stock.location',
            string='Destination Location',
            compute='_get_transfer_locations',
            store=True)


    @api.one
    @api.onchange('product_id')
    def product_id_change(self):
        self.product_uom_id = self.product_id.uom_id and self.product_id.uom_id.id or False

    @api.multi
    @api.depends('transfer.source_warehouse', 'transfer.dest_warehouse')
    def _get_transfer_locations(self):
        for rec in self:
            rec.source_location = rec.transfer.source_warehouse.lot_stock_id.id
            dest_location = False
            transit_locations = self.env['stock.location'].search(
                    [
                        ('usage', '=', 'transit')
                    ]
            )
            for location in transit_locations:
                if location.get_warehouse(location) == rec.transfer.dest_warehouse.id:
                    dest_location = location.id

            if not dest_location:
                rec.dest_location = rec.transfer.dest_warehouse.lot_stock_id.id
            else:
                rec.dest_location = dest_location

    @api.multi
    def get_move_vals(self, picking, group):
        """
        Get the correct move values
        :param picking:
        :param group:
        :return: dict
        """

        self.ensure_one()
        return {
            'name' : 'Warehouse Transfer',
            'product_id' : self.product_id.id,
            'product_uom' : self.product_uom_id.id,
            'product_uom_qty' : self.product_qty,
            'location_id' : self.source_location.id,
            'location_dest_id' : self.dest_location.id,
            'picking_id' : picking.id,
            'group_id': group.id,
            'note': self.note
        }

