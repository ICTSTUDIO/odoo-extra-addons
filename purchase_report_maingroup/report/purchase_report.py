# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import tools, models, fields, api

class PurchaseReport(models.Model):
    _inherit = 'purchase.report'

    product_maincategory = fields.Many2one(
        comodel_name='product.category',
        string='Top Level Category', readonly=True)
    product_secondcategory = fields.Many2one(
        comodel_name='product.category',
        string='2nd Level Category', readonly=True)
    product_thirdcategory = fields.Many2one(
        comodel_name='product.category',
        string='3th Level Category', readonly=True)

    def _select(self):
        return super(PurchaseReport, self)._select(
        ) + " , t.main_category as product_maincategory, t.second_category as product_secondcategory, t.third_category as product_thirdcategory"

    def _group_by(self):
        return super(PurchaseReport, self)._group_by(
        ) + " , t.main_category, t.second_category, t.third_category"
