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
        #If this works it can be placed in a seperate module orderpoint_merge / closed_planner
        if self.purchase_id:
            if 'closed_planner' in self.purchase_id._fields:
                if self.purchase_id.closed_planner:
                    _logger.debug("Closed Planner: %s", self.purchase_id)
                    return True
        check_moves = self.move_ids
        for origmove in self.move_ids:
            if origmove.move_dest_id:
                _logger.debug("Found Dest Move: %s", origmove.move_dest_id)
                check_moves = check_moves | origmove.move_dest_id

        for move in check_moves:
            if move.picking_id:
                #If this works it can be placed in a seperate module orderpoint_merge / warehouse_transfer
                if 'transfer' in move.picking_id._fields:
                    if move.picking_id.transfer:
                        _logger.debug("Warehouse Transfer: %s", move.picking_id.transfer)
                        return True
                #If this works it can be placed in a seperate module orderpoint_merge / linked_group for assigned warehouse push
                if 'linked_group' in move.picking_id._fields:
                    if move.picking_id.linked_group and move.picking_id.group_id:
                        _logger.debug("Linked Group: %s", move.picking_id.group_id)
                        return True
        return False

    @api.multi
    def get_chained_procurements(self):
        cps = self

        # Get all chained procurements
        for rec in self:
            for move in rec.move_ids:
                cps = cps | move.procurement_id
                cps = cps | move.move_dest_id.procurement_id.get_chained_procurements()
            cps = cps.filtered(lambda p: p.state not in ('cancel', 'done'))

        # Check chained procurements on cancel blocks
        for chained_procurement in cps:
            if chained_procurement.check_no_cancel():
                # If this is true cancellation of this procurement is prohibited so remove from returned procurements
                cps = cps - chained_procurement
        _logger.debug("Chained Procurements: %s", cps)
        return cps

    @api.multi
    def cancel_procurement(self):
        for rec in self:
            _logger.debug("Cancelling Proc: %s", rec)
            rec.cancel_chain()
            for move in rec.move_ids:
                if move.state == 'cancel':
                    _logger.debug("Removing Moves: %s", move)
                    move.unlink()

    @api.multi
    def cancel_chain(self):
        error_procurements = self.env['procurement.order']
        cancel_procurements = self.env['procurement.order']
        for rec in self:
            if rec.state not in ('cancel', 'done'):
                _logger.debug("Proc State: %s", rec.state)
                if rec.check_no_cancel():
                    _logger.debug("Prevented Cancel: %s", rec)
                    error_procurements += rec
                else:
                    rec.cancel()
                    cancel_procurements += rec
        return cancel_procurements, error_procurements
