# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    dropship_address = fields.Many2one(
            comodel_name='dropship.address',
            related='group_id.dropship_address',
            string='Dropship Address',
            store=True
    )