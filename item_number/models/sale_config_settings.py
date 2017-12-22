# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields


class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    module_item_number = fields.Boolean(
            string='Item Numbers from Sale Order Line to Invoice',
            help="""This module will allow you to maintain a correct line number for each Line."""
    )
