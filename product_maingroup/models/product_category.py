# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.category"

    main_category = fields.Many2one(
            comodel_name='product.category',
            string="Top Level Category",
            compute="get_main_category",
            store=True
    )

    @api.multi
    @api.depends('parent_id')
    def get_main_category(self):
        for rec in self:
            main_category = rec._get_main_category()
            rec.main_category = main_category
    
    @api.model
    def calc_main_category(self):
        if self.parent_id:
            return self.parent_id.calc_main_category()
        return self
    
    @api.multi
    def _get_main_category(self):
        self.ensure_one()
        return self.calc_main_category()
        
