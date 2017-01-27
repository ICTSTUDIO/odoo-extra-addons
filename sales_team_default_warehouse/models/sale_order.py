# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warehouse_id = fields.Many2one(
            compute="_get_section_default_warehouse",
            store=True
    )

    @api.one
    @api.depends('section_id')
    def _get_section_default_warehouse(self):
        if self.section_id.default_warehouse:
            self.warehouse_id = self.section_id.default_warehouse

    @api.model
    def _prepare_invoice(self, order, lines):
        vals = super(SaleOrder, self)._prepare_invoice(order, lines)
        if order.section_id:
            vals['section_id'] = order.section_id.id

        return vals