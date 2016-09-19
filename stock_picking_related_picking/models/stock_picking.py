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

    @api.one
    @api.depends('group_id')
    def get_related_pickings(self):
        group_pickings = self.env['stock.picking']
        for group in self.group_id:
            group_pickings = group_pickings | self.search([('group_id', '=', group.id)])

        related_pickings = group_pickings - self
        _logger.debug("Related Pickings: %s", related_pickings)
        if related_pickings:
            self.related_pickings = related_pickings


    @api.one
    @api.depends('related_pickings')
    def _get_related_pickings_name(self):
        self.related_pickings_name = ', '.join([rp.name for rp in self.related_pickings])


