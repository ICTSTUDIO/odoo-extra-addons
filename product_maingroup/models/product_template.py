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
    
    @api.depends('categ_id', 'categ_id.main_category', 'categ_id.second_category', 'categ_id.third_category')
    @api.multi
    def get_main_category(self):
        for rec in self:
            if rec.categ_id:
                rec.main_category = rec.categ_id.main_category
                rec.second_category = rec.categ_id.second_category
                rec.third_category = rec.categ_id.third_category
            else:
                rec.main_category = False
                rec.second_category = False
                rec.third_category = False
