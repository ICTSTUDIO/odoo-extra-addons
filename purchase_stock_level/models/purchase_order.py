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

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    priority = fields.Selection(
            selection=[('urgent', 'Urgent'), ('normal', 'Normaal'), ('none', 'Geen')],
            compute="_get_priority",
            search="_search_priority",
            string="Priority"
    )

    def _search_priority(self, operator, value):
        po_ids =[]
        for order in self.search([('state', 'not in', ['cancel', 'done'])]):
            if operator == '=':
                if order.priority == value:
                    po_ids.append(order.id)
            if operator == 'in':
                if order.priority in value:
                    po_ids.append(order.id)
        return [('id', 'in', po_ids)]

    @api.one
    @api.depends('order_line.priority')
    def _get_priority(self):
        count = {'urgent': 0, 'normal': 0}
        for line in self.order_line:
            if line.priority == 'urgent':
                count['urgent'] += 1
            if line.priority == 'normal':
                count['normal'] += 1

        if count['urgent'] > 0:
            self.priority = 'urgent'
        elif count['normal'] > 0:
            self.priority = 'normal'
        else:
            self.priority = 'none'
