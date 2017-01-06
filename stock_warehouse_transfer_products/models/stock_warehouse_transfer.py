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


class StockWarehouseTransfer(models.Model):
    _name = 'stock.warehouse.transfer'
    _description = 'Stock Warehouse Transfer'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].get('stock.warehouse.transfer')

    @api.model
    def _get_default_date(self):
        return fields.Date.context_today(self)

    @api.model
    def _get_default_state(self):
        return 'draft'

    @api.multi
    @api.depends('pickings.state')
    def _calc_transfer_state(self):
        for rec in self:
            if rec.pickings:
                picking_states = [p.state for p in rec.pickings]
                if 'done' in picking_states:
                    rec.state = 'done'
                else:
                    rec.state = 'picking'

            else:
                rec.state = 'draft'

    name = fields.Char(
            string='Reference',
            default=_get_default_name)
    date = fields.Date(
            string='Date',
            default=_get_default_date)
    source_warehouse = fields.Many2one(
            comodel_name='stock.warehouse',
            string='Source Warehouse')
    dest_warehouse = fields.Many2one(
            comodel_name='stock.warehouse',
            string='Destination Warehouse')
    state = fields.Selection(
            selection=[
                ('draft', 'Draft'),
                ('picking', 'Picking'),
                ('done', 'Done')],
            string='Status',
            default=_get_default_state,
            store=True,
            compute=_calc_transfer_state)
    lines = fields.One2many(
            comodel_name='stock.warehouse.transfer.line',
            inverse_name='transfer',
            string='Transfer Lines')
    pickings = fields.One2many(
            comodel_name='stock.picking',
            inverse_name='transfer',
            string='Related Picking')
    company_id = fields.Many2one(
            comodel_name='res.company', string='Company', required=True,
            default=lambda self: self.env['res.company']._company_default_get(
                    'stock.warehouse.transfer'))


    def get_transfer_picking_type(self):
        self.ensure_one()

        picking_types = self.env['stock.picking.type'].search(
                [
                    ('default_location_src_id', '=', self.source_warehouse.lot_stock_id.id),
                    ('code', '=', 'outgoing')
                ]
        )
        if not picking_types:
            _logger.error("No picking tye found")
            #TODO: Exception Raise

        return picking_types and picking_types[0]

    @api.multi
    def get_picking_vals(self):
        self.ensure_one()
        picking_type = self.get_transfer_picking_type()
        picking_vals = {
            'picking_type_id' : picking_type.id,
            'transfer' : self.id,
            'origin': self.name
        }

        return picking_vals

    @api.multi
    def action_create_picking(self):
        for rec in self:
            picking_vals = rec.get_picking_vals()
            _logger.debug("Picking Vals: %s", picking_vals)
            picking = rec.pickings.create(picking_vals)
            if not picking:
                _logger.error("Error Creating Picking")
                #TODO: Add  Exception

            pc_group = rec._get_procurement_group()

            for line in rec.lines:
                move_vals = line.get_move_vals(picking, pc_group)
                if move_vals:
                    _logger.debug("Move Vals: %s", move_vals)
                    self.env['stock.move'].create(move_vals)

            picking.action_confirm()
            picking.action_assign()

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