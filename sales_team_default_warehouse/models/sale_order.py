# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warehouse_id = fields.Many2one(
            compute="_get_team_default_warehouse",
            store=True
    )

    @api.depends('team_id')
    def _get_team_default_warehouse(self):
        if self.team_id.default_warehouse:
            self.warehouse_id = self.team_id.default_warehouse

    @api.model
    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        if self.team_id:
            vals['team_id'] = self.team_id.id

        return vals