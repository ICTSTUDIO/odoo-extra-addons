# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit="purchase.order.line"

    product_stock_stock = fields.Float(
            compute='get_stock'
    )
    product_stock_incoming = fields.Float(
            compute='get_stock'
    )
    product_stock_outgoing = fields.Float(
            compute='get_stock'
    )
    product_stock_virtual = fields.Float(
            compute='get_stock'
    )
    product_stock_web = fields.Float(
            compute='get_web_stock'
    )

    priority = fields.Selection(
        selection=[('urgent', 'Urgent'), ('high','Hoog'), ('normal', 'Normaal'), ('none', 'Geen')],
        compute="get_priority",
        string="Priority"
    )

    @api.multi
    @api.depends('product_stock_outgoing', 'product_stock_stock')
    def get_web_stock(self):
        for rec in self:
            rec._get_web_stock()

    def _get_web_stock(self):
        self.product_stock_web = self.product_stock_stock - self.product_stock_outgoing

    @api.multi
    @api.depends('product_id', 'order_id.picking_type_id.default_location_dest_id')
    def get_stock(self):
        for rec in self:
            rec._get_stock()

    def _get_stock(self):
        if self.order_id.picking_type_id and self.order_id.picking_type_id.default_location_dest_id:
            product = self.env['product.product'].with_context(
                {'location': self.order_id.picking_type_id.default_location_dest_id.id}
            ).browse(self.product_id.id)
        else:
            product = self.product_id

        self.product_stock_stock = product.qty_available
        self.product_stock_incoming = product.incoming_qty
        self.product_stock_outgoing = product.outgoing_qty
        self.product_stock_virtual = product.virtual_available

    @api.multi
    @api.depends('product_stock_web')
    def get_priority(self):
        for rec in self:
            rec._get_priority()

    def _get_priority(self):
        if self.order_id.state not in ('done','cancel','except_picking','except_invoice','approved'):
            if self.product_stock_web < 0 and self.product_stock_virtual < 0:
                self.priority = 'urgent'
            elif self.product_stock_web < 0 and self.product_stock_virtual >= 0:
                self.priority = 'high'
            else:
                self.priority = 'normal'
        else:
            self.priority = 'none'
