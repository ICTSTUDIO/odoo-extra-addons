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

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit="purchase.order.line"

    product_stock_stock = fields.Float(
            compute='_get_stock'
    )
    product_stock_incoming = fields.Float(
            compute='_get_stock'
    )
    product_stock_outgoing = fields.Float(
            compute='_get_stock'
    )
    product_stock_web = fields.Float(
            compute='_get_web_stock'
    )

    priority = fields.Selection(
        selection=[('urgent', 'Urgent'), ('normal', 'Normaal'), ('none', 'Geen')],
        compute="_get_priority",
        string="Priority"
    )

    @api.one
    @api.depends('product_stock_outgoing', 'product_stock_stock')
    def _get_web_stock(self):
            self.product_stock_web = self.product_stock_stock - self.product_stock_outgoing

    @api.one
    @api.depends('product_id', 'order_id.location_id')
    def _get_stock(self):
        product = self.env['product.product'].with_context(
                {'location': self.order_id.location_id.id}
        ).browse(self.product_id.id)

        self.product_stock_stock = product.qty_available
        self.product_stock_incoming = product.incoming_qty
        self.product_stock_outgoing = product.outgoing_qty

    @api.one
    @api.depends('product_stock_web')
    def _get_priority(self):
        if self.order_id.state not in ('done','cancel','except_picking','except_invoice','approved'):
            if self.product_stock_web < 0:
                self.priority = 'urgent'
            else:
                self.priority = 'normal'
        else:
            self.priority = 'none'