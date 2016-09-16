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
from openerp import models, fields, api, _
from openerp import workflow

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    auto_invoice = fields.Selection(
            selection=[
                ('no', 'No Automatic Invoice'),
                ('yes', 'Automatic Invoice'),
                ('valid', 'Automatic Invoice & Validation'),

            ],
            string='Auto Invoice on Delivery',
            default='no'
    )
    auto_invoiced = fields.Boolean(
        string='Automaticly Invoiced',
        compute='_get_auto_invoice',
        store=True
    )

    @api.one
    @api.depends('order_line.move_ids.state')
    def _get_auto_invoice(self):
        ctx2 = dict(self._context, auto_invoice=self.id)
        if self._context.get('auto_invoice') and self._context.get('auto_invoice') == self.id:
            _logger.debug("Purchase Order: %s Already Invoiced", self.id)
        if self.auto_invoice in ['yes', 'valid'] and self.invoice_method == 'manual':
            if all([move.state in ['cancel', 'done'] for move in [line.move_ids for line in self.order_line]]):
                ctx = dict(ctx2, inv_type='in_invoice')

                if self.auto_invoice == 'valid':
                    self.sudo().with_context(ctx).create_and_validate_invoice(validate=True)
                else:
                    self.sudo().with_context(ctx).create_and_validate_invoice()
                self.auto_invoiced = True


    @api.multi
    def create_and_validate_invoice(self, validate=False):
        self.ensure_one()
        invoices = self.action_invoice_create()
        _logger.debug("Invoices: %s", invoices)

        if isinstance(invoices, (int, long)):
            invoices = [invoices]

        if validate:
            for invoice in invoices:
                _logger.debug('Validating Invoice: %s',(invoice))
                workflow.trg_validate(
                        self.sudo()._uid,
                        'account.invoice',
                        invoice,
                        'invoice_open',
                        self._cr
                )