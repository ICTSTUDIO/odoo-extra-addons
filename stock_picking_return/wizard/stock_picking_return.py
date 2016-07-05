# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import models, api, fields, _
from openerp.exceptions import ValidationError


class StockPickingReturn(models.TransientModel):
    _name = 'stock.picking.return'
    _description = 'Picking Return'

    return_lines = fields.One2many(
            comodel_name='stock.picking.return.line',
            inverse_name='return_id',
            string='Moves'
    )
    move_dest_exists = fields.Boolean(
            string='Chained Move Exists',
            readonly=True,
            help="Technical field used to hide help tooltip if not needed"
    )
    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Original Picking"
    )
    invoice_state = fields.Selection(
            selection=[
                ('2binvoiced', 'To be refunded/invoiced'),
                ('none', 'No invoicing')
            ],
            string='Invoicing',
            required=True
    )

    @api.model
    def default_get(self, fields):
        if self.env.context.get('active_ids', False):
            if len(self.env.context.get('active_ids')) > 1:
                raise ValidationError(_('Warning!'), _("You may only return one picking at a time!"))
        res = super(StockPickingReturn, self).default_get(fields)
        record_id = self.env.context.get('active_id', False) or False
        res['picking_id'] = record_id
        pick = self.env['stock.picking'].browse(record_id)
        if pick:
            if 'invoice_state' in fields:
                if pick.invoice_state=='invoiced':
                    res.update({'invoice_state': '2binvoiced'})
                else:
                    res.update({'invoice_state': 'none'})
        return res

    @api.multi
    def _create_returns(self):
        returned_lines = 0

        # Cancel assignment of existing chained assigned moves
        moves_to_unreserve = []
        for move in self.picking_id.move_lines:
            to_check_moves = [move.move_dest_id] if move.move_dest_id.id else []
            while to_check_moves:
                current_move = to_check_moves.pop()
                if current_move.state not in ('done', 'cancel') and current_move.reserved_quant_ids:
                    moves_to_unreserve.append(current_move.id)
                split_moves = self.env['stock.move'].search(
                        [
                            ('split_from', '=', current_move.id)
                        ]
                )
                if split_moves:
                    to_check_moves += self.env['stock.move'].browse(split_moves.ids)

        if moves_to_unreserve:
            unreserve_moves = self.env['stock.move'].browse(moves_to_unreserve)
            unreserve_moves.do_unreserve()
            #break the link between moves in order to be able to fix them later if needed
            unreserve_moves.write(
                    {'move_orig_ids': False}
            )

        #Create new picking for returned products
        pick_type_id = self.picking_id.picking_type_id.return_picking_type_id and self.picking_id.picking_type_id.return_picking_type_id.id or self.picking_id.picking_type_id.id
        new_picking = self.picking_id.copy(
                {
                    'move_lines': [],
                    'picking_type_id': pick_type_id,
                    'state': 'draft',
                    'origin': self.picking_id.name,
                }
        )

        for line in self.return_lines:
            move = line.move_id
            if not move:
                raise ValidationError(_('Warning !'), _("You have manually created product lines, please delete them to proceed"))
            new_qty = line.quantity
            if new_qty:
                # The return of a return should be linked with the original's destination move if it was not cancelled
                if move.origin_returned_move_id.move_dest_id.id and move.origin_returned_move_id.move_dest_id.state != 'cancel':
                    move_dest_id = move.origin_returned_move_id.move_dest_id.id
                else:
                    move_dest_id = False

                returned_lines += 1
                line_values = {
                    'product_id': line.product_id.id,
                    'product_uom_qty': new_qty,
                    'product_uos_qty': new_qty * move.product_uos_qty / move.product_uom_qty,
                    'picking_id': new_picking.id,
                    'state': 'draft',
                    'location_id': move.location_dest_id.id,
                    'location_dest_id': move.location_id.id,
                    'picking_type_id': pick_type_id,
                    'warehouse_id': self.picking_id.picking_type_id.warehouse_id.id,
                    'origin_returned_move_id': move.id,
                    'procure_method': 'make_to_stock',
                    'restrict_lot_id': line.lot_id.id,
                    'move_dest_id': move_dest_id,
                }

                if self.invoice_state == '2binvoiced':
                    line_values['invoice_state'] = '2binvoiced'

                line.move_id.copy(line_values)

        if not returned_lines:
            raise ValidationError(_('Warning!'), _("Please specify at least one non-zero quantity."))

        new_picking.action_confirm()
        new_picking.action_assign()
        return new_picking, pick_type_id

    @api.multi
    def create_returns(self):
        """
         Creates return picking.
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param ids: List of ids selected
         @param context: A standard dictionary
         @return: A dictionary which of fields with values.
        """
        new_picking, pick_type_id = self._create_returns()
        # Override the context to disable all the potential filters that could have been set previously
        ctx = {
            'search_default_picking_type_id': pick_type_id,
            'search_default_draft': False,
            'search_default_assigned': False,
            'search_default_confirmed': False,
            'search_default_ready': False,
            'search_default_late': False,
            'search_default_available': False,
        }
        return {
            'domain': "[('id', 'in', [" + str(new_picking.id) + "])]",
            'name': _('Returned Picking'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'context': ctx,
        }