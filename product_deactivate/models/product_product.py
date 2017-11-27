# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def button_deactivate(self):
        for rec in self:
            if rec.active:
                resp, message = rec._check_deactivate()
                if resp:
                    rec.active = False
                else:
                    raise Warning(_('Deactivation Not Allowed'), message)

    @api.model
    def _check_deactivate(self):
        """
        Deactivation Check, return True to allow deactivation
        :return: AllowDeactivate (boolean), ErrorMEssage
        """
        if self.virtual_available:
            return False, _('Virtual Stock Available')
        if self.qty_available:
            return False, _('Stock Available')
        return True, False




