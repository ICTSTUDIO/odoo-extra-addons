# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        self.send_order_email()
        return res

    @api.model
    def _mail_automation(self):
        return False

    @api.model
    def _get_mail_template(self):
        return False
    
    @api.multi
    def send_order_email(self):
        for record in self:
            if self._mail_automation():
                template = self._get_mail_template()
                if template:
                    template.send_mail(
                        record.id,
                        # force_send=True,
                    )
