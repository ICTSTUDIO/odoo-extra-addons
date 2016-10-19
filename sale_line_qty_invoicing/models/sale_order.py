# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _make_invoice(self, order, lines):
        if order.order_policy=='picking':
            inv_obj = self.env['account.invoice']
            inv = self._prepare_invoice(order, lines)
            invoice = inv_obj.create(inv)
            data = invoice.onchange_payment_term_date_invoice(inv['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
            if data.get('value', False):
                invoice.write(data['value'])
            invoice.button_compute()
            return invoice.id
        else:
            return super(SaleOrder, self)._make_invoice(order, lines)