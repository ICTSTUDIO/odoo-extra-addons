# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import api, models

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'base.kanban.abstract']

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        stage = self.stage_id.search([], order="sequence asc", limit=1)
        default.update({'stage_id': stage.id})
        return super(SaleOrder, self).copy(default=default)
