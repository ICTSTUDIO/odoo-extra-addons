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
         compute="get_related_pickings",
    )

    @api.model
    def _get_related_pickings(self):
        related_pickings = self
        if self.group_id:
            for group in self.group_id:
                related_pickings = related_pickings | self.search(
                    [
                        ('group_id', '=', group.id)
                    ]
                )
        else:
            orig_pickings = self.mapped('move_lines.move_orig_ids.picking_id')
            dest_pickings = self.mapped('move_lines.move_dest_id.picking_id')
            related_pickings = orig_pickings | dest_pickings

        return related_pickings - self

    @api.model
    def _get_related_pickings_name(self):
        return ', '.join([rp.name for rp in self.related_pickings])

    @api.multi
    @api.depends('move_lines', 'group_id')
    def get_related_pickings(self):
        for rec in self:
            rec.related_pickings = rec._get_related_pickings()
            rec.related_pickings_name = rec._get_related_pickings_name()




