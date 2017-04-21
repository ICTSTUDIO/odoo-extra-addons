# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def action_view_sale_report(self):
        act_obj = self.pool.get('ir.actions.act_window')
        mod_obj = self.pool.get('ir.model.data')
        result = mod_obj.xmlid_to_res_id(self._cr, self._uid, 'product_sale_report.act_product_2_sale_report',raise_if_not_found=True)
        result = act_obj.read(self._cr, self._uid, [result], context=self._context)[0]
        result['domain'] = "[('product_id','in',[" + ','.join(map(str, self.ids)) + "])]"
        result['context'] = "{'search_default_Sales':1, 'search_default_sales_team_sales_qty': 1}"
        return result

