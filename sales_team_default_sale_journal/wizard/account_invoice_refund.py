# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.model
    def _get_journal(self):
        journal = super(AccountInvoiceRefund, self)._get_journal()
        active_id = self._context and self._context.get('active_id', False)
        _logger.debug('ActiveID: %s', active_id)
        if active_id:
            invoice = self.env['account.invoice'].browse(active_id)
            if invoice.section_id and invoice.section_id.default_sale_refund_journal:
                _logger.debug('Journal: %s', invoice.section_id.default_sale_refund_journal)
                journal = invoice.section_id.default_sale_refund_journal.id
        return journal

    journal_id = fields.Many2one(
        default=lambda self: self._get_journal()
    )

