# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import tools, models, fields, api

class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

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
        return super(AccountInvoiceReport, self)._select(
        ) + " , sub.product_maincategory as product_maincategory, sub.product_secondcategory as product_secondcategory, sub.product_thirdcategory as product_thirdcategory"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select(
        ) + " , pt.main_category as product_maincategory, pt.second_category as product_secondcategory, pt.third_category as product_thirdcategory"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by(
        ) + " , pt.main_category, pt.second_category, pt.third_category"
