# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    moves_available_count = fields.Integer(
            string='Available Moves',
            compute='_get_moves_count',
    )
    moves_waiting_count = fields.Integer(
            string='Waiting Moves',
            compute='_get_moves_count',
    )

    @api.one
    @api.depends('move_lines')
    def _get_moves_count(self):
        self.moves_available_count = self.move_lines.search_count(
                [
                    ('state', '=', 'assigned'),
                    ('picking_id', '=', self.id)
                ]
        )
        self.moves_waiting_count = self.move_lines.search_count(
                [
                    ('state', '=', 'confirmed'),
                    ('picking_id', '=', self.id)
                ]
        )