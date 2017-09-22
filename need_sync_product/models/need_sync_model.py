# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncModel(models.Model):
    _inherit = "need.sync.model"

    def _select_models(self):
        list_models = super(NeedSyncModel, self)._select_models()
        list_models.append(('product.product', 'Product'))
        return list_models

    model = fields.Selection(
            selection=_select_models,
            string="Model",
            required=True,
            index=True
    )

    def get_products_from_template(self, product_templates):
        return self.env['product.product'].search(
                [
                    ('product_tmpl_id', 'in', product_templates.ids)
                ]
        )

    def get_products_from_category(self, product_categories):
        return self.env['product.product'].search(
                [
                    ('categ_id', 'in', product_categories.ids)
                ]
        )

    def get_products_from_pricelist(self):
        changed_price_product_records = self.env['product.pricelist.item'].search(
                [
                    ('write_date', '>', self.last_check_date),
                    ('product_id', '!=', False)

                ]
        )
        products = changed_price_product_records.mapped('product_id')

        changed_price_product_templ_records = self.env['product.pricelist.item'].search(
                [
                    ('write_date', '>', self.last_check_date),
                    ('product_tmpl_id', '!=', False)

                ]
        )
        product_templates = changed_price_product_templ_records.mapped('product_tmpl_id')

        changed_price_product_categ_records = self.env['product.pricelist.item'].search(
                [
                    ('write_date', '>', self.last_check_date),
                    ('categ_id', '!=', False)
                ]
        )
        product_categories = changed_price_product_categ_records.mapped('categ_id')
        return products | self.get_products_from_template(product_templates) | self.get_products_from_category(product_categories)

    def get_products_from_stock_moves(self):
        changed_stock_moves = self.env['stock.move'].search(
                [
                    ('write_date', '>', self.last_check_date),
                    ('product_id', '!=', False)
                ]
        )
        return changed_stock_moves.mapped('product_id')

    @api.multi
    def get_object_records_changed(self):
        """
        Detect Object Changes
        :return: list of res_id
        """
        self.ensure_one()

        changed_records = super(NeedSyncModel, self).get_object_records_changed()
        if self.model == 'product.product':
            changed_template_records = self.env['product.template'].search(
                    [
                        ('write_date', '>', self.last_check_date)
                    ]
            )
            if changed_template_records:
                changed_records = changed_records | self.get_products_from_template(changed_template_records)

            changed_records = changed_records | self.get_products_from_pricelist()

            changed_records = changed_records | self.get_products_from_stock_moves()

        return changed_records
