# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import models, api


class StockMoveCancel(models.TransientModel):
    _name = 'stock.move.cancel'
    _description = "Cancel Stock Moves"

    @api.one
    def cancel_moves(self):
        stock_move_obj = self.env['stock.move']
        active_ids = self.env.context.get('active_ids', [])
        for move in stock_move_obj.browse(active_ids):
            move.action_cancel()
        return True
