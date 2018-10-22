# -*- coding: utf-8 -*-
# Copyright© 2017-today ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def print_labels_get_lines(self):
        label_list = []
        for rec in self:
            label_list.append([0,0,{
                'product_id': rec.id,
                'quantity': 1
            }])
        return label_list

    @api.multi
    def print_labels_get_label(self):
        label_lines = self.print_labels_get_lines()
        if label_lines:
            vals = {'label_lines': label_lines}
            return self.env['product.product.label'].create(vals)
        return self.env['product.product.label']


    @api.multi
    def print_labels(self):
        label = self.print_labels_get_label()
        if label:
            return label.print_labels()
        return False

    @api.multi
    def print_labels_medium(self):
        label = self.print_labels_get_label()
        if label:
            return label.print_labels_medium()
        return False

    @api.multi
    def print_labels_small(self):
        label = self.print_labels_get_label()
        if label:
            return label.print_labels_small()
        return False