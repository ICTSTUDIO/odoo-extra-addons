# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    supplier_status = fields.Selection(
        selection=[
            ('done', 'Done'),
            ('draft', 'Define at least 1 supplier'),
            ('exception', 'No Supplier with sequence 1 defined'),
            ('double', 'More than 1 Supplier with sequence 1 defined'),
            ('price_exception', 'Default Supplier without price')
        ],
        compute='get_supplier_status',
        default='draft',
        store=True
    )

    @api.multi
    @api.depends('seller_ids')
    def get_supplier_status(self):
        for rec in self:
            status = 'done'
            if rec.seller_ids == False:
                status = 'draft'
            else:
                supplier_sellers = rec.seller_ids.filtered(
                    lambda r: r.sequence == 1)
                if len(supplier_sellers) < 1:
                    status = 'exception'
                elif len(supplier_sellers) > 1:
                    status = 'double'
                elif len(supplier_sellers) == 1 and supplier_sellers.filtered(
                        lambda r: r.supplier_price == False):
                    status = 'price_exception'
            rec.supplier_status = status
