# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import models, fields
from openerp import tools

_logger = logging.getLogger(__name__)

class StockMoveLocation(models.Model):
    _inherit = "stock.move.location"

    related_pickings_name = fields.Char(
            related='picking_id.related_pickings_name',
            string='Related'
    )