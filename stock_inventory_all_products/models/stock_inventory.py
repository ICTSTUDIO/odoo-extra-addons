# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import _, api, fields, models

class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.model
    def _get_inventory_lines_values(self):
        self.ensure_one()
        vals = []
        product_obj = self.env['product.product']
        inventory = self.new(self._convert_to_write(self.read()[0]))
        if self.filter == 'none':
            products = product_obj.search([('type', 'not in', ('service', 'consu', 'digital'))])
            for product in products:
                inventory.product_id = product
                vals += super(StockInventory,
                              inventory)._get_inventory_lines_values()

        else:
            vals = super()._get_inventory_lines_values()
        return vals
