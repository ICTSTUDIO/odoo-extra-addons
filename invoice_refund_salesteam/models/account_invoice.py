# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
        vals = super(AccountInvoice, self)._prepare_refund(
                invoice, date=date, period_id=period_id,
                description=description, journal_id=journal_id
        )

        if invoice.section_id:
            vals['section_id'] = invoice.section_id.id

        return vals
