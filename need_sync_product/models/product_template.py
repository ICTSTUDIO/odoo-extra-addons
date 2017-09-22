# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    need_sync_count = fields.Integer(
            related='product_variant_ids.need_sync_count'
    )
    need_sync_total = fields.Integer(
            related='product_variant_ids.need_sync_total'
    )
    need_sync_connections = fields.One2many(
        comodel_name="need.sync.connection",
        string="Need Sync Connections",
        related="product_variant_ids.need_sync_connections"
    )


    @api.multi
    def open_need_sync(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'

        filter_domain = [
            ('res_id', 'in', self.product_variant_ids.ids),
            ('model', '=', 'product.product')
        ]

        return {
            'name': _('Open Need Sync'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'need.sync.line',
            'src_model': 'product.product',
            'target': 'current',
            'ctx': {'search_default_filter_sync_needed':1},
            'domain': filter_domain
        }

    @api.multi
    def unlink(self):
        products = self.env['product.product'].browse(self.ids)
        self.env['need.sync'].unlink_records('product.product', products.ids)
        return super(ProductTemplate, self).unlink()
