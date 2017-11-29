# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def _need_sync_lines_published(self):
        return self.env['need.sync.line'].search(
            [
                ('model', '=', str(self._model)),
                ('res_id', '=', self.id),
                ('published', '=', True)
            ]
        )
        
        
    @api.model
    def _check_deactivate(self):
        """
        Total override of method because of change in stock check
        :return: AllowDeactivate (boolean), ErrorMEssage
        """
        if self._need_sync_lines_published():
            return False, _('Need Sync Lines Published')
        if self.need_sync_count:
            return False, _('Need Sync Lines Require Update')
        
        return super(ProductProduct, self)._check_deactivate()
