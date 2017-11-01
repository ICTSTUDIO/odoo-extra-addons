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
        for move in self.move_ids:
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
        chained_procurements = self.env['procurement.order']
        for rec in self:
            for move in rec.move_ids:
                chained_procurements += move.procurement_id
                chained_procurements += move.move_dest_id.procurement_id.get_chained_procurements()
            chained_procurements = chained_procurements.filtered(lambda p: p.state not in ('cancel', 'done'))
            for chained_procurement in chained_procurements:
                if chained_procurement.check_no_cancel():
                    _logger.debug("Removing from Chained Proc: %s", chained_procurement)
                    chained_procurements -= chained_procurement
        _logger.debug("Chained Procurements: %s", chained_procurements)
        return chained_procurements

    @api.multi
    def cancel_procurement(self):
        for rec in self:
            _logger.debug("Cancelling Proc: %s", rec)
            rec.cancel()
            if rec.purchase_id and rec.purchase_id.state == 'cancel':
                _logger.debug("Removing Purchase Order: %s", rec.purchase_id)
                rec.purchase_id.unlink()
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
