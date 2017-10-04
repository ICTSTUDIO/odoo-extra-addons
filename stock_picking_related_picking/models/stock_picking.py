# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    related_pickings = fields.Many2many(
        comodel_name='stock.picking',
        compute="get_related_pickings",
        string="Related Pickings"
    )
    related_pickings_name = fields.Char(
         string='Related Pickings Name',
         compute='_get_related_pickings_name',
    )

    @api.multi
    @api.depends('move_lines', 'group_id')
    def get_related_pickings(self):
        for rec in self:
            related_pickings = rec
            if rec.group_id:
                for group in rec.group_id:
                    related_pickings = related_pickings | self.search(
                        [
                            ('group_id', '=', group.id)
                        ]
                    )
            else:
                orig_pickings = rec.mapped('move_lines.move_orig_ids.picking_id')
                dest_pickings = rec.mapped('move_lines.move_dest_id.picking_id')
                related_pickings = orig_pickings | dest_pickings

            _logger.debug("Related Pickings: %s", related_pickings)
            related_pickings = related_pickings - self
            rec.related_pickings = related_pickings

    @api.multi
    @api.depends('related_pickings')
    def _get_related_pickings_name(self):
        for rec in self:
            rec.related_pickings_name = ', '.join([rp.name for rp in rec.related_pickings])


