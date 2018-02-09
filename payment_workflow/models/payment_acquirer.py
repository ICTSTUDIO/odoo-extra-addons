# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    payment_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Payment Journal"
    )

    payment_workflow = fields.Boolean(
        string="Payment Workflow",
        default=False,
        help="When active a invoice with payment will be generated after "
             "receiving the payment from acquirer. Order Policy needs to be "
             "manual to work.")
