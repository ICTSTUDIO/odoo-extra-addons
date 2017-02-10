# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        vals = super(StockPicking, self)._get_invoice_vals(key, inv_type, journal_id, move)

        if move.picking_id.section_id and inv_type in ('out_invoice', 'out_refund'):
            if move.picking_id.section_id.default_sale_journal:
                vals['journal_id'] = move.picking_id.section_id.default_sale_journal.id

        return vals