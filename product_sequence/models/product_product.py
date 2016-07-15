# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp import models, fields, api, _
from openerp.exceptions import Warning, ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"


    default_code = fields.Char(default='[Auto]')


    @api.multi
    @api.constrains('default_code')
    def _check_code(self):
        ctx = dict(self._context, active_test=False)

        for product in self:
            if product.default_code:
                products = self.with_context(ctx).search(
                        [
                            ('default_code','=',product.default_code)
                        ]
                )
                if products and len(products)>1:
                    raise ValidationError(_("Default Code already exists!"))

    @api.model
    def get_default_code(self):
        default_code=False
        while True:
            default_code = self.env['ir.sequence'].get('product.product')
            if self.search([('default_code','=', default_code)]):
                _logger.warning("Default Code already in use getting new code!")
            else:
                _logger.debug("Code: %s", default_code)
                break
        return default_code

    @api.model
    def create(self, vals):
        ctx = dict(self._context, active_test=False)

        # Check if sequence exists and assign new number to product
        if vals.get('default_code', '[Auto]') == '[Auto]':
            vals['default_code'] = self.with_context(ctx).get_default_code()

        if vals.get('default_code', '[Auto]') == '[Auto]':
             raise Warning(
                 _('No product sequence is defined'))

        return super(ProductProduct, self).create(vals)
