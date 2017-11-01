# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.multi
    def action_cancel_chain(self):
        for rec in self:
            chained_procurements = rec.procurement_ids.get_chained_procurements()
            _logger.debug("Chained Procurements: %s", chained_procurements)
            cancel_procurements, error_procurements = chained_procurements.cancel_chain()
            if error_procurements:
                _logger.debug("Errors: %s", error_procurements)
            if cancel_procurements:
                _logger.debug("Cancel: %s", cancel_procurements)
        return True