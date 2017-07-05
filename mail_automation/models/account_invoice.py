# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        self.send_invoice_email()
        return res

    @api.model
    def _mail_automation(self):
        return False
    
    @api.model
    def _get_mail_template(self):
        return False
        
    @api.multi
    def send_invoice_email(self):
        for record in self:
            if self._mail_automation():
                template = self._get_mail_template()
                if template:
                    message = template.send_mail(
                        record.id,
                        # force_send=True,
                    )
                    if message:
                        record.sent = True