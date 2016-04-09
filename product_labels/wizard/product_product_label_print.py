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

from openerp import models, fields, api


class ProductProductLabel(models.TransientModel):
    _name = "product.product.label"

    label_lines = fields.One2many(
            comodel_name='product.product.label.line',
            inverse_name='label_id',
            string='Labels'
    )

    @api.model
    def default_get(self, fields):
        res = super(ProductProductLabel, self).default_get(fields)
        label_lines = self.lines_get()
        res['label_lines'] = label_lines
        return res

    @api.multi
    def lines_get(self):
        context = self._context or {}
        products = self.env['product.product'].browse(context.get('active_ids', []))
        label_list = []
        for product in products:
            label_list.append([0,0,{
                'product_id': product.id,
                'quantity': 1
            }])
        return label_list

    @api.multi
    def print_labels(self):
        records = self
        return self.env['report'].get_action(records,
                                             'product_labels.product_product_label'
                                             )


class ProductProductLabelLine(models.TransientModel):
    _name = "product.product.label.line"

    label_id = fields.Many2one(
        comodel_name="product.product.label",
        string="Product Label"
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product"
    )
    quantity = fields.Integer(string="Label Qty", default=1)

    @api.one
    def get_label_data(self):
        return {
            'label_id': self.label_id.id,
            'name': self.product_id.name,
            'code': self.product_id.default_code or False,
            'barcode': self.product_id.ean13 or False,
        }
