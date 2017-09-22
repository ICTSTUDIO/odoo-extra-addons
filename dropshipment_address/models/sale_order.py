# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import urllib
import logging
from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    dropship_address = fields.Many2one(
            comodel_name='dropship.address',
            string='Dropship Address',
    )

    @api.model
    def _prepare_procurement_group(self, order):
        res = super(SaleOrder, self)._prepare_procurement_group(order)
        if res and order.dropship_address:
            res['dropship_address'] = order.dropship_address.id
        return res