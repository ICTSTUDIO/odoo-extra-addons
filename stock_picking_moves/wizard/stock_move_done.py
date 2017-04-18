# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import models, api


class StockMoveDone(models.TransientModel):
    _name = 'stock.move.done'
    _description = "Finalize Stock Moves"

    @api.one
    def finalize_moves(self):
        stock_move_obj = self.env['stock.move']
        active_ids = self.env.context.get('active_ids', [])
        for move in stock_move_obj.browse(active_ids):
            if move.state == 'assigned':
                move.action_done()
        return True
