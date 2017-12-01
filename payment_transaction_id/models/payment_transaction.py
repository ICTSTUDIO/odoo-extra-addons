# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    base_transaction_state = fields.Selection(
        selection=[('draft','Draft'),('done','Done')],
        string="Base Transaction State",
        default='draft',
        compute="get_base_transaction_state"
    )

    @api.multi
    @api.depends('sale_order_id', 'acquirer_reference')
    def get_base_transaction_state(self):
        for rec in self:
            if rec.order_id and rec.aquirer_reference:
                if rec.order_id.transaction_id != rec.acquirer_reference:
                    rec.order_id.transaction_id = rec.acquirer_reference
            rec.base_transaction_state = 'done'
