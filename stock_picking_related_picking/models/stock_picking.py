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

    related_pickings_count = fields.Integer(
        compute="compute_related_pickings_count",
        string="Number Related Pickings"
    )

    @api.multi
    def compute_related_pickings_count(self):
        for rec in self:
            rec.related_pickings_count = len(rec.related_pickings)

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

    @api.multi
    def open_related_pickings(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'

        filter_domain = [
            ('id', 'in', self.related_pickings.ids)
        ]
        if self.related_pickings and len(self.related_pickings) >= 1:
            return {
                'name': _('Related Pickings') + ": %s" % (self.name),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'stock.picking',
                'src_model': 'stock.picking',
                'target': 'current',
                'domain': filter_domain
            }
        elif self.related_pickings and len(self.related_pickings) == 1:
            return {
                'name': _('Related Pickings') + ": %s" % (self.name),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form, tree',
                'res_model': 'stock.picking',
                'src_model': 'stock.picking',
                'target': 'current',
                'domain': filter_domain
            }

