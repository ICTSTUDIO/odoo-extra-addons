# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp import workflow

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

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
    @api.depends('order_line.procurement_ids.state')
    def _get_auto_invoice(self):
        ctx2 = dict(self._context, auto_invoice=self.id)
        if self._context.get('auto_invoice') and self._context.get('auto_invoice') == self.id:
            _logger.debug("Sale Order: %s Already Invoiced", self.id)
    
        group = self.procurement_group_id

        if group and self.auto_invoice in ['yes', 'valid'] and self.order_policy == 'manual':
            if all([proc.state in ['cancel', 'done'] for proc in group.procurement_ids]):
                ctx = dict(ctx2, inv_type='out_invoice')

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