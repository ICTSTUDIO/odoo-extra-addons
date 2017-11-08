# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    linked_group = fields.Boolean(
            string="Linked Procurement Group",
            default=False
    )

    @api.multi
    def action_assign(self):
        self.create_linked_group()
        return super(StockPicking, self).action_assign()

    @api.multi
    def rereserve_pick(self):
        self.create_linked_group()
        return super(StockPicking, self).rereserve_pick()

    @api.multi
    def action_done(self):
        self.create_linked_group()
        return super(StockPicking, self).action_done()

    @api.multi
    def action_confirm(self):
        self.create_linked_group()
        return super(StockPicking, self).action_confirm()

    @api.multi
    def force_assign(self):
        """ Changes state of picking to available if moves are confirmed or waiting.
        @return: True
        """

        self.create_linked_group()

        return super(StockPicking, self).force_assign()

    @api.multi
    def create_linked_group(self):

        for rec in self:
            if 'related_pickings' in rec._fields:
                for picking in rec.related_pickings:
                    if not rec.linked_group and picking.linked_group:
                        rec.linked_group = True
            if rec.linked_group:
                pc_group = rec._get_procurement_group()
                _logger.debug("Group: %s", pc_group)
                move_group_ids = [x.id for x in rec.move_lines if x.state not in ('done')]
                pickings = self.env['stock.picking']
                for move in rec.move_lines:
                    for orig in move.move_orig_ids:
                        move_group_ids.append(orig.id)
                        if orig.picking_id:
                            pickings = pickings | orig.picking_id
                    if move.move_dest_id:
                        move_group_ids.append(move.move_dest_id.id)
                        if move.move_dest_id.picking_id:
                            pickings = pickings | move.move_dest_id.picking_id

                grouped_moves = self.env['stock.move'].browse(move_group_ids)
                grouped_moves.write({'group_id': pc_group.id})
                _logger.debug("Move IDS: %s", move_group_ids)
                _logger.debug("Pickings: %s", pickings)
                for picking in pickings:
                    if picking != rec:
                        _logger.debug("Setting Linkded Group on Related Picking: %s", picking)
                        picking.linked_group = True
                        picking.group_id = pc_group.id
                        if 'manual_assign' in rec._fields and rec.manual_assign:
                            picking.manual_assign = True




    @api.model
    def _prepare_procurement_group(self):
        return {'name': self.name}

    @api.model
    def _get_procurement_group(self):
        pc_groups = self.env['procurement.group'].search(
                [
                    ('name', '=', self.name)
                ]
        )
        if pc_groups:
            pc_group = pc_groups[0]
        else:
            pc_vals = self._prepare_procurement_group()
            pc_group = self.env['procurement.group'].create(pc_vals)
        return pc_group or False

