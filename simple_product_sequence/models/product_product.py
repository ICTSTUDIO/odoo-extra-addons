# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import api, models, fields, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(
        default='[Auto]',
        index=True
    )

    @api.one
    @api.constrains('default_code')
    def _check_default_code(self):
        if self.default_code:
            code_products = self.search(
                [
                    ('default_code', '=', self.default_code)
                ]
            )
            if len(code_products) >= 1:
                if not self in code_products or len(code_products) > 1:
                    raise ValidationError(_('Error !'),
                                          _('Default Code is already used for other product'))

    @api.model
    def create(self, vals):
        # Check if sequence exists and assign new number to product
        if vals.get('default_code', '[Auto]') == '[Auto]':
            while True:
                vals['default_code'] = self.env['ir.sequence'].next_by_code('product.product')
                if self.search([('default_code', '=', vals['default_code'])]):
                    _logger.debug("product get next by code product.product code already exists in database")
                else:
                    break

        if vals.get('default_code', '[Auto]') == '[Auto]':
             raise ValidationError(
                 _('Error !'),
                 _('No product sequence is defined'))

        return super(ProductProduct, self).create(vals)
