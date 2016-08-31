# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def get_chained_procurements(self):
        chained_procurements = self.env['procurement.order']
        for rec in self:
            for move in rec.move_ids:
                _logger.debug("move.procurement_id: %s", move.procurement_id)
                chained_procurements += move.procurement_id
                chained_procurements += move.move_dest_id.procurement_id.get_chained_procurements()
            chained_procurements += rec
        return chained_procurements

    @api.multi
    def cancel_chain(self):
        error_procurements = self.env['procurement.order']
        cancel_procurements = self.env['procurement.order']
        for rec in self:
            try:
                _logger.debug("Proc State: %s", rec.state)
                if rec.state not in ('cancel', 'done'):
                    rec.cancel()
                    cancel_procurements += rec
            except:
                _logger.error("Cancel Procurement Failed: %s", rec)
                error_procurements += rec
        return cancel_procurements, error_procurements
