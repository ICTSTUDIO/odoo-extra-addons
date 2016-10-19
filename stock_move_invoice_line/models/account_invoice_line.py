# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp import workflow

_logger = logging.getLogger(__name__)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    sale_line_id = fields.Many2one(
            related='move_id.sale_line_id',
            string='Sale Order Line',
            readonly=True,
            store=True,
            ondelete='set null'
    )
