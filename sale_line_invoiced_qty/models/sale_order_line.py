# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_invoiced = fields.Float(
            compute="_get_inv_qty",
            digits=dp.get_precision('Product Unit of Measure'),
            string='Invoiced',
            #store=True,
            help="Quantity Invoiced")


    @api.model
    def _get_real_qty(self, inv_line):
        return self.product_uom._compute_qty_obj(
                inv_line.uos_id,
                inv_line.quantity,
                self.product_uom
        )

    @api.model
    def check_invoice(self, inv_line):
        # Check Invoice states
        if inv_line.invoice_id.state not in ('draft', 'open', 'done'):
            return False

        # Check Date Filters
        if all([self._context.get('date_start'), self._context.get('date_stop')]):
            invoice = inv_line.invoice_id
            if not (invoice.date_invoice >= self._context['date_start'] and
                            invoice.date_invoice <= self._context['date_stop']):
                return False
        return True

    @api.one
    @api.depends('invoice_lines')
    def _get_inv_qty(self):
            qty_invoiced = 0
            for inv_line in self.invoice_lines:
                if self.check_invoice(inv_line):
                    # Add Quantity
                    qty_invoiced += self._get_real_qty(inv_line)
            self.qty_invoiced = qty_invoiced