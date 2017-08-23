# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_invoiced = fields.Float(compute="_invoice_total", string="Total Invoiced", groups='account.group_account_invoice')

    @api.multi
    def _invoice_total(self):
        ctx = dict(self._context, active_test=False)
        return super(ResPartner, self.with_context(ctx))._invoice_total(field_name="total_invoiced", arg=None)
