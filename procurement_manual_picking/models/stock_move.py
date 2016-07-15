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

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_assign(self):
        to_assign=[]
        for rec in self:
            if rec.picking_id and rec.picking_id.manual_assign:
                if not self.env.context.get('no_assign_manual'):
                    to_assign.append(rec.id)
            else:
                to_assign.append(rec.id)

        to_assign_rec = self.browse(to_assign)
        super(StockMove, to_assign_rec).action_assign()

    @api.model
    def _prepare_picking_assign(self, move):
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited.
        """
        values = super(StockMove, self)._prepare_picking_assign(move)
        if move.rule_id and move.rule_id.manual_assign:
            values['manual_assign'] = True
        return values