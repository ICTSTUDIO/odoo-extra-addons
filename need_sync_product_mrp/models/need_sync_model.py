# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncModel(models.Model):
    _inherit = "need.sync.model"


    def get_products_from_bom(self, cproducts):
        products = self.env['product.product']

        bomlines = self.env['mrp.bom.line'].search(
                [
                    ('product_id', 'in', cproducts.ids)
                ]
        )
        _logger.debug("BOMlineS %s:", bomlines)
        boms = bomlines.mapped('bom_id')
        _logger.debug("BOMS %s:", boms)
        if boms:
            products = boms.mapped('product_id')
            _logger.debug("BOMS Products %s:", products)
            product_templates = boms.mapped('product_tmpl_id')
            _logger.debug("BOMS ProductsTempl %s:", product_templates)
            if product_templates:
                products = products | product_templates.mapped('product_variant_ids')
            _logger.debug("BOM Products: %s", products)
        return products

    @api.multi
    def get_object_records_changed(self):
        self.ensure_one()
        changed_records = super(NeedSyncModel, self).get_object_records_changed()
        _logger.debug("Object Records: %s", changed_records)
        if self.model == 'product.product':
            changed_records = changed_records | self.get_products_from_bom(changed_records)
        return changed_records
