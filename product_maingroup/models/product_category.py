# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.category"

    main_category = fields.Many2one(
            comodel_name='product.category',
            string="Top Level Category",
            compute="get_main_category",
            store=True
    )

    second_category = fields.Many2one(
        comodel_name='product.category',
        string="2nd Level Category",
        compute="get_main_category",
        store=True
    )

    third_category = fields.Many2one(
        comodel_name='product.category',
        string="3th Level Category",
        compute="get_main_category",
        store=True
    )

    @api.multi
    @api.depends('parent_id')
    def get_main_category(self):
        for rec in self:
            main_category, second_category, third_category = rec._get_main_category()
            rec.main_category = main_category
            rec.second_category = second_category
            rec.third_category = third_category


    @api.model
    def _get_category_structure(self, inv_level=0, category_structure={}):
        inv_level += 1
        category_structure[inv_level] = self

        if self.parent_id:
            category_structure, inv_level = self.parent_id._get_category_structure(inv_level, category_structure)

        return category_structure, inv_level

    @api.model
    def _parse_category_structure(self, category_structure, level):
        category_123 = {}
        category_123[1] = category_structure[level]
        category_123[2] = False
        category_123[3] = False
        if (level - 1) > 0:
            category_123[2] = category_structure[level-1]
        if (level -2) > 0:
            category_123[3] = category_structure[level-2]

        return category_123

    
    @api.multi
    def _get_main_category(self):
        self.ensure_one()
        category_structure, level = self._get_category_structure()
        if category_structure and level:
            category_123 = self._parse_category_structure(category_structure, level)
            if category_123:
                return category_123[1], category_123[2], category_123[3]

        return self, False, False
        
