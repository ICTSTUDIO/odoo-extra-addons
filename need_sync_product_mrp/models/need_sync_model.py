# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncModel(models.Model):
    _inherit = "need.sync.model"


    def get_products_from_bom(self, cproducts):
        products = self.env['product.product']

        boms = self.env['mrp.bom.line'].search(
                [
                    ('product_id', 'in', cproducts.ids)
                ]
        )
        if boms:
            products = boms.mapped('product_id')
            product_templates = boms.mapped('product_tmpl_id')
            if product_templates:
                products = products | product_templates.mapped('product_variant_ids')

        return products

    @api.multi
    def get_object_records_changed(self):
        self.ensure_one()
        changed_records = super(NeedSyncModel, self).get_object_records_changed()
        if self.model == 'product.product':
            changed_records = changed_records | self.get_products_from_bom(changed_records)
        return changed_records
