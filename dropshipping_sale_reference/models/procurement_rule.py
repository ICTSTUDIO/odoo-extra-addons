# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from odoo import models, fields, api, _


_logger = logging.getLogger(__name__)

class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def _prepare_purchase_order(self, product_id, product_qty, product_uom, origin, values, partner):
        return_values = super(ProcurementRule, self)._prepare_purchase_order(product_id, product_qty, product_uom, origin, values, partner)
        return_values.update({'dest_address_ref': values.get('partner_dest_ref', False)})
        return return_values