# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.multi
    def open_related_moves(self):
        """ Open the Related Stock Moves
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        _logger.debug("Product_id: %s", self.product_id)
        ctx = dict(
                search_default_product_id=self.product_id,
                search_default_location_id=self.lot_stock_id.id
        )

        return {
            'name': _('Open Related Stock Moves'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.move.location',
            'src_model': 'stock.warehouse',
            # 'views': [(compose_form.id, 'form')],
            # 'view_id': compose_form.id,
            'target': 'current',
            'context': ctx,
        }
