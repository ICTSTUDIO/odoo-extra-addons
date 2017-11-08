# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def check_no_cancel(self):
        self.ensure_one()
        no_cancel = super(ProcurementOrder, self).check_no_cancel()
        _logger.debug("Check no Cancel Transit")
        if not no_cancel:
            if self.rule_id and self.rule_id.prevent_cancel:
                transit_move = self.env['stock.move'].search(
                    [
                        ('procurement_id', '=', self.id)
                    ],
                    limit=1
                )
                if transit_move and transit_move.move_dest_id and transit_move.move_dest_id.procurement_id and transit_move.move_dest_id.procurement_id.state == 'done':
                    _logger.debug("Check no Cancel Transit: True")
                    return True
        return no_cancel
