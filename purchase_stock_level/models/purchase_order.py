# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    priority = fields.Selection(
            selection=[('urgent', 'Urgent'), ('high', 'Hoog'), ('normal', 'Normaal'), ('none', 'Geen')],
            compute="get_priority",
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


    @api.multi
    @api.depends('order_line.priority')
    def get_priority(self):
        for rec in self:
            rec._get_priority()

    def _get_priority(self):
        count = {'urgent': 0, 'high': 0, 'normal': 0}
        for line in self.order_line:
            if line.priority == 'urgent':
                count['urgent'] += 1
            if line.priority == 'high':
                count['high'] += 1
            if line.priority == 'normal':
                count['normal'] += 1

        if count['urgent'] > 0:
            self.priority = 'urgent'
        elif count['high'] > 0:
            self.priority = 'high'
        elif count['normal'] > 0:
            self.priority = 'normal'
        else:
            self.priority = 'none'
