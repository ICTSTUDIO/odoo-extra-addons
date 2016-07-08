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

    # @api.multi
    # def _picking_assign(self, procurement_group, location_from, location_to):
    #     """Assign a picking on the given move_ids, which is a list of move supposed to share the same procurement_group, location_from and location_to
    #     (and company). Those attributes are also given as parameters.
    #     """
    #     _logger.debug('Picking Assign')
    #     return_value = super(StockMove, self)._picking_assign(procurement_group, location_from, location_to)
    #
    #     for rec in self:
    #         if rec.move_dest_id:
    #             _logger.debug("Existing Dest Move")
    #
    #             orig = rec.move_dest_id
    #             _logger.debug("Original Move: %s", orig)
    #             if orig.picking_id and orig.picking_id.linked_group:
    #                 pc_group = self._get_procurement_group(orig.picking_id)
    #                 _logger.debug("Verwerving Groep: %s", pc_group)
    #                 rec.group_id = pc_group.id
    #                 if rec.picking_id and not rec.picking_id.group_id:
    #                     rec.picking_id.group_id = pc_group.id
    #
    #     return return_value


    @api.model
    def _prepare_picking_assign(self, move):
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited.
        """
        values = super(StockMove, self)._prepare_picking_assign(move)
        if move.rule_id and move.rule_id.linked_group:
            values['linked_group'] = True
        return values

    # @api.model
    # def _prepare_procurement_from_move(self, move):
    #     res = super(StockMove, self)._prepare_procurement_from_move(move)
    #     _logger.debug("Passing Values: %s", res)
    #     if move.picking_id and move.picking_id.linked_group:
    #         pc_group = self._get_procurement_group(move.picking_id)
    #         res['group_id'] = pc_group.id
    #
    #     return res