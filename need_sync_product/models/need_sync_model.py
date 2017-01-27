# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp import models, fields, api

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

    def get_products_from_template(self, product_templates):
        return self.env['product.product'].search(
                [
                    ('product_tmpl_id', 'in', product_templates.ids)
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
        return products | self.get_products_from_template(product_templates)

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
