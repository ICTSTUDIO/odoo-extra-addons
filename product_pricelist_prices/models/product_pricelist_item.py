# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.multi
    def change_product(self):

        for rec in self:
            if rec.product_tmpl_id:
                rec.product_tmpl_id.write({'write_uid': self._uid})
            if rec.product_id:
                rec.product_id.write({'write_uid': self._uid})

        return True

    @api.multi
    def unlink(self):
        self.change_product()
        return super(ProductPricelistItem, self).unlink()

    @api.multi
    def write(self, vals):
        ret = super(ProductPricelistItem, self).write(vals)
        self.change_product()
        return ret

    @api.model
    def create(self, vals):
        items = super(ProductPricelistItem, self).create(vals)
        if items:
            items.change_product()
        return items
