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

    @api.cr_uid_ids_context
    def _picking_assign(self, cr, uid, move_ids, procurement_group, location_from, location_to, context=None):
        """Assign a picking on the given move_ids, which is a list of move supposed to share the same procurement_group, location_from and location_to
        (and company). Those attributes are also given as parameters.
        """

        if any([move.rule_id and move.rule_id.separate_product for move in self.browse(cr, uid, move_ids, context=context)]):
            for move_id in move_ids:
                move = self.browse(cr, uid, move_id, context=context)
                picking_id = move._picking_assign_separate_product(procurement_group, location_from, location_to)
                if picking_id:
                    move.picking_id = picking_id
                    _logger.debug("Created Separate Picking: %s", picking_id)
        else:
            return super(StockMove, self)._picking_assign(
                    cr,
                    uid,
                    move_ids,
                    procurement_group,
                    location_from,
                    location_to,
                    context=context
            )

    @api.model
    def _picking_assign_separate_product(self, procurement_group, location_from, location_to):
        picking = self.env['stock.picking']

        # Use a SQL query as doing with the ORM will split it in different queries with id IN (,,)
        # In the next version, the locations on the picking should be stored again.
        query = """
            SELECT stock_picking.id FROM stock_picking, stock_move
            WHERE
                stock_picking.state in ('draft', 'confirmed', 'waiting') AND
                stock_move.picking_id = stock_picking.id AND
                stock_move.location_id = %s AND
                stock_move.location_dest_id = %s AND
                stock_move.product_id = %s AND
        """
        params = (location_from, location_to, self.product_id.id)
        if not procurement_group:
            query += "stock_picking.group_id IS NULL LIMIT 1"
        else:
            query += "stock_picking.group_id = %s LIMIT 1"
            params += (procurement_group,)
        self.env.cr.execute(query, params)
        picking_id = self.env.cr.fetchone() or False
        if not picking_id:
            values = self._prepare_picking_assign(self)
            pick = picking.create(values)
            if pick:
                picking_id = pick.id
            else:
                picking_id = False
        return picking_id