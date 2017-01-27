# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    need_sync_count = fields.Integer(
        compute="compute_sync_count",
        string="To Sync Products"
    )
    need_sync_total = fields.Integer(
            compute="compute_sync_count",
            string="Total Sync Entries"
    )

    @api.one
    def compute_sync_count(self):
        _logger.debug("Model: %s", self._model)
        need_sync_lines = self.env['need.sync.line'].search(
                [
                    ('model', '=', str(self._model)),
                    ('res_id', '=', self.id),
                ]
        )
        self.need_sync_count = len(
                need_sync_lines.filtered(lambda b: b.sync_needed)
        )
        self.need_sync_total = len(need_sync_lines)

    @api.multi
    def open_need_sync(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'

        filter_domain = [
            ('res_id', '=', self.id),
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