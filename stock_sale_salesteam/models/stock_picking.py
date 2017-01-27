# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    section_id = fields.Many2one(
            compute='_get_section_id',
            search='_search_section_id',
            comodel_name='crm.case.section',
            string='Sales Team'
    )

    @api.one
    @api.depends('group_id')
    def _get_section_id(self):
        if self.sale_id and self.sale_id.section_id:
            self.section_id = self.sale_id.section_id


    def _search_section_id(self, operator, value):
        res = []
        picking_ids = []
        assert operator in ('=', 'in'), 'Invalid domain operator'
        assert isinstance(value, (float, int)), 'Invalid domain right operand'

        sale_orders = self.env['sale.order'].search(
                [
                    ('section_id', operator, value),
                    ('procurement_group_id', '!=', False)
                ]
        )
        group_ids = []
        for order in sale_orders:
            group_ids.append(order.procurement_group_id.id)
        _logger.debug('GroupIds: %s', group_ids)

        stock_pickings = self.search([
            ('group_id', 'in', group_ids)
        ])
        for picking in stock_pickings:
            picking_ids.append(picking.id)

        res.append(('id', 'in', picking_ids))
        return res