# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp import workflow

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _paymentworkflow_get_account_from_journal(self, journal_id):
        journal = self.env['account.journal'].browse(journal_id)
        if journal:
            return journal.default_credit_account_id and journal.default_credit_account_id.id or journal.default_debit_account_id and journal.default_debit_account_id.id or False
        return False
    
    @api.model
    def _paymentworkflow_register_payment(self, invoice, journal_id, amount, account_id=None,
                               reference=None, writeoff_account_id=None,
                               writeoff_period_id=None, writeoff_journal_id=None):
        if not account_id:
            account_id = self._paymentworkflow_get_account_from_journal(journal_id)
        if not reference:
            reference = invoice.number
        period = invoice.period_id
        if not writeoff_journal_id:
            writeoff_journal_id = journal_id
        if not writeoff_period_id:
            writeoff_period_id = period.id
        if not writeoff_account_id:
            writeoff_account_id = invoice.account_id.id

        _logger.debug("Registering Payment: %s", invoice)

        if period:
            _logger.debug("Payment Reference: %s", reference)
            invoice.pay_and_reconcile(
                amount,
                account_id,
                period.id,
                journal_id,
                writeoff_account_id,
                writeoff_period_id,
                writeoff_journal_id,
                name=reference
            )
        else:
            _logger.error("Error Registering Payment")
        return True

    
    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        # Trigger invoice creation and payment registration
        if self.payment_tx_id:
            if self.payment_tx_id.state=='done' and self.payment_acquirer_id.payment_workflow and self.order_policy == 'manual':

                inv_ids = self.manual_invoice()
                if inv_ids:
                    invoice_id = inv_ids['res_id']
                    _logger.debug('Created invoice: %s', str(invoice_id))

                invoice = self.env['account.invoice'].browse(invoice_id)
            
                _logger.debug("Validating Invoice: %s", invoice)

                workflow.trg_validate(
                    self.sudo()._uid,
                    'account.invoice',
                    invoice.id,
                    'invoice_open',
                    self._cr
                )
                _logger.debug("Validated Invoice: %s", invoice)
                
                if invoice and invoice.state == 'open':
                    # Build extra checks
                    reference = self.payment_tx_id.acquirer_reference
                    journal_id = self.payment_acquirer_id.payment_journal_id and self.payment_acquirer_id.payment_journal_id.id
                    amount = self.payment_tx_id.amount or 0.0
                    self._paymentworkflow_register_payment(invoice, journal_id, amount, reference=reference)
        return res
