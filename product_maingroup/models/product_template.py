# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    main_category = fields.Many2one(
            comodel_name='product.category',
            string="Top Level Category",
            compute="get_main_category",
            store=True
    )
    
    @api.depends('categ_id', 'categ_id.main_category')
    @api.multi
    def get_main_category(self):
        for rec in self:
            rec.main_category = rec._get_main_category()
    
    @api.multi
    def _get_main_category(self):
        self.ensure_one()
        if self.categ_id:
            return self.categ_id.main_category
        return False
        
