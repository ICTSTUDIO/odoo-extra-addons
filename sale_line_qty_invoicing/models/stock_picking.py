# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def set_move_invoice_state(self):
        if self.sale_id:
            for picking in self.sale_id.picking_ids:
                for move in picking.move_lines:
                    if move.state not in ['cancel','done']:
                        move.invoice_state = '2binvoiced'

    @api.multi
    def action_invoice_create(self, journal_id, group=False, type='out_invoice'):
        if self.sale_id:
            invoice_ids = []
            inv_id = self.sale_id.action_invoice_create()
            self.set_move_invoice_state()
            _logger.debug("Created Invoices: %s", inv_id)
            if isinstance(inv_id, (long, int)):
                invoice_ids.append(inv_id)
            elif isinstance(inv_id, list):
                invoice_ids += inv_id
            return invoice_ids
        else:
            return super(StockPicking, self).action_invoice_create(journal_id, group=group, type=type)
