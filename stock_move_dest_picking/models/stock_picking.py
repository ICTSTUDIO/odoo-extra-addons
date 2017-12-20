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
        self.check_related_linked_group()
        return super(StockPicking, self).action_assign()

    @api.multi
    def rereserve_pick(self):
        self.check_related_linked_group()
        return super(StockPicking, self).rereserve_pick()

    @api.multi
    def action_done(self):
        self.check_related_linked_group()
        return super(StockPicking, self).action_done()

    @api.multi
    def action_confirm(self):
        self.check_related_linked_group()
        return super(StockPicking, self).action_confirm()

    @api.multi
    def force_assign(self):
        """ Changes state of picking to available if moves are confirmed or waiting.
        @return: True
        """

        self.check_related_linked_group()

        return super(StockPicking, self).force_assign()

    @api.model
    def check_related_linked_group(self, pickings=None, group=None):
        for rec in self:
            rec._check_related_linked_group(pickings=pickings, group=group)

    @api.model
    def get_related_field_list(self):
        return ['linked_group', 'manual_assign', 'shop_transfer']

    @api.model
    def _check_related_linked_group(self, pickings=None, group=None):
        if not pickings:
            pickings = self.env['stock.picking']
        
        if 'related_pickings' in self._fields:
            pickings = self.related_pickings | pickings

        pickings = pickings - self

        if group:
            if not self.group_id or (self.group_id and self.group_id.id != group.id):
                self.group_id = group.id

        for picking in pickings:
            if not self.linked_group and picking.linked_group:
                self.linked_group = True
            elif self.linked_group and not picking.linked_group:
                picking.linked_group = True
                
            if 'manual_assign' in self._fields and self.manual_assign:
                if not self.manual_assign and picking.manual_assign:
                    self.manual_assign = True
                elif self.manual_assign and not picking.manual_assign:
                    picking.manual_assign = True

            if 'manual_assign' in self._fields and self.manual_assign:
                if not self.manual_assign and picking.manual_assign:
                    self.manual_assign = True
                elif self.manual_assign and not picking.manual_assign:
                    picking.manual_assign = True
            
            if group:
                if not picking.group_id or (picking.group_id and picking.group_id.id != group.id):
                    picking.group_id = group.id

    @api.multi
    def create_linked_group(self):
        for rec in self:
            rec._create_linked_group()
            
    @api.multi
    def _create_linked_group(self):
        if self.linked_group:
            pc_group = self._get_procurement_group()
            _logger.debug("Group: %s", pc_group)
            move_group_ids = [x.id for x in self.move_lines if x.state not in ('done')]
            pickings = self.env['stock.picking']
            for move in self.move_lines:
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
            
            self.check_related_linked_group(pickings, pc_group)
            
            # for picking in pickings:
            #     if picking != self.
            #         _logger.debug("Setting Linkded Group on Related Picking: %s", picking)
            #         picking.linked_group = True
            #         picking.group_id = pc_group.id
            #         if 'manual_assign' in self._fields and self.manual_assign:
            #             picking.manual_assign = True




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

