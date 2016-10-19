# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    invoiced = fields.Boolean(
            compute="_get_invoiced",
            string='Invoiced',
            store=True
    )

    @api.model
    def _prepare_order_line_invoice_line(self, line, account_id=False):
        vals = super(SaleOrderLine, self)._prepare_order_line_invoice_line(line, account_id=account_id)
        if line.order_id.order_policy=='picking' and vals:
            if not line.invoiced:

                vals['price_unit'] = line.price_unit
        return vals

    @api.one
    def _get_invoiced(self):
        self.invoiced = False
        if self.order_id.order_policy == 'picking':
            if self.qty_invoiced >= self.qty_delivered:
                self.invoiced = True
        else:
            if self.qty_invoiced >= self.product_uom_qty:
                self.invoiced = True

    @api.model
    def _get_line_qty(self, line):
        if line.order_id.order_policy == 'manual':
            return super(SaleOrderLine, self)._get_line_qty(line)
        elif line.order_id.order_policy == 'picking':
            _logger.debug("Qty Invoiced: %s", line.qty_invoiced)
            _logger.debug("Qty Delivered: %s", line.qty_delivered)
            qty_to_invoice = line.qty_delivered - line.qty_invoiced
            _logger.debug("Qty To Invoice: %s", qty_to_invoice)
            return qty_to_invoice

