# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging
from openerp import api, models, _
from openerp.tools.float_utils import float_round
from openerp.addons.report_xls.utils import rowcol_to_cell, _render

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    @api.multi
    def _compute_cost_and_qty_available_at_date(self):
        # logic based on _product_available method from standard addons
        res = {}
        for category in self:
            products = self.env['product.product'].search(
                [
                    ('main_category', '=', category.id),
                    # '|',
                    # ('active','=', True),
                    # ('active','=',False)
                ]
            )
            for product in products:
                prod_res = product._compute_cost_and_qty_available_at_date()
                if prod_res[product.id] and prod_res[product.id][0] and prod_res[product.id][1]:
                    if res.get(category.id):
                        res[category.id] += prod_res[product.id][0] * prod_res[product.id][1]
                    else:
                        res[category.id] = prod_res[product.id][0] * prod_res[product.id][1]
        return res


    @api.model
    def _stock_level_export_xls_fields(self):
        return [
            # Inventory fields
            'name',
            # Stock Valuation fields
            'stock_value',
        ]

    @api.model
    def stock_level_export_xls_template(self):
        """
        Template updates, e.g.

        res = super(ProductProduct, self).stock_level_export_xls_template()
        _logger.debug("Res: %s", res)
        res.update({
            'main_category': {
                'header': [1, 42, 'text', _('Top Level Category')],
                'products': [1, 0, 'text', _render("product.main_category.name or ''")],
                'totals': [1, 0, 'text', None]},
        })
        return res
        """
        return {}

