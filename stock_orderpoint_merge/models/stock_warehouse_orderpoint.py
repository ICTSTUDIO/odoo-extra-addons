# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import api, models

_logger = logging.getLogger(__name__)

class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.model
    def subtract_procurements(self, orderpoint):

        qty_before = self.env['procurement.order']._product_virtual_get(orderpoint)
        for procurement in orderpoint.procurement_ids:
            no_cancel = False
            if procurement.state in ('cancel', 'done'):
                continue
            for move in procurement.move_ids:
                if move.state not in ('draft', 'waiting'):
                    no_cancel = True

            if procurement.check_no_cancel():
                no_cancel = True

            if not no_cancel:
                _logger.debug("Cancel Procurement: %s", procurement)
                procurement.cancel_procurement()

        qty_after = self.env['procurement.order']._product_virtual_get(orderpoint)
        return super(StockWarehouseOrderpoint, self).subtract_procurements(orderpoint) + qty_after - qty_before