# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_id = fields.Many2one(
            compute='_get_sale_id',
            comodel_name='sale.order',
            store=True,
            index=True
    )

    @api.one
    @api.depends('group_id')
    def _get_sale_id(self):
        if self.group_id:
            sale_orders = self.env['sale.order'].search(
                    [
                        ('procurement_group_id', '=', self.group_id.id)
                    ]
            )
            self.sale_id = sale_orders and sale_orders[0].id

    _