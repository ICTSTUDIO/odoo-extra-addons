# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"


    @api.multi
    def write(self, values):
        if values.get('route_ids'):
            self.cancel_all_chained_procurements()
        return super(ProductProduct, self).write(values)

    @api.model
    def cancel_all_chained_procurements(self):
        orderpoints = self.env['stock.warehouse.orderpoint'].search([('product_id', 'in', self.ids)])
        orderpoints.action_cancel_chain()
        return True