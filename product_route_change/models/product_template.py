# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"


    @api.multi
    def write(self, values):
        if values.get('route_ids'):
            for rec in self:
                for product in rec.product_variant_ids:
                    product.cancel_all_chained_procurements()
        return super(ProductTemplate, self).write(values)