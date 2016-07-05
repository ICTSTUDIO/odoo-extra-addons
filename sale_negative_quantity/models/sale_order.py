# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
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

import logging

from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _prepare_order_line_procurement(self, order, line, group_id=False):
        vals = super(SaleOrder, self)._prepare_order_line_procurement(order, line, group_id=group_id)
        if line.product_uom_qty < 0:
            if vals.get('route_ids'):
                del vals['route_ids']
            if order.warehouse_id.return_rule_id:
                vals['rule_id'] = order.warehouse_id.return_rule_id.id
            vals['product_qty'] = -line.product_uom_qty
            vals['product_uos_qty'] = line.product_uos and -line.product_uos_qty or -line.product_uom_qty
            vals['location_id'] = order.warehouse_id.lot_stock_id.id
        return vals