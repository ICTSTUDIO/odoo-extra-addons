# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp import models, api, fields
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class StockPickingReturnLine(models.TransientModel):
    _name = "stock.picking.return.line"
    _rec_name = 'move_id'

    product_id = fields.Many2one(
            comodel_name='product.product',
            string="Product",
            required=True
    )
    quantity = fields.Float(
            string="Quantity",
            digits_compute=dp.get_precision('Product Unit of Measure'),
            required=True
    )
    return_id = fields.Many2one(
            comodel_name='stock.picking.return',
            string="Wizard"
    )
    move_id = fields.Many2one(
            comodel_name='stock.move',
            string="Move"
    )
    lot_id = fields.Many2one(
            comodel_name='stock.production.lot',
            string='Serial Number',
            help="Used to choose the lot/serial number of the product returned"
    )

    @api.onchange('move_id')
    def onchange_move_id(self):
        self.product_id = self.move_id.product_id
        self.quantity = self.move_id.product_qty