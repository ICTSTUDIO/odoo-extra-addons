# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.category"
    
    need_sync_connections = fields.One2many(
        comodel_name="need.sync.connection",
        string="Need Sync Connections",
        compute="_get_need_sync_connection",
        inverse="_set_need_sync_connection"
    )

    @api.one
    def _get_need_sync_connection(self):
        """
        Only show connections on Partner with model activated
        :return: 
        """
        need_sync_connection_models = self.env['need.sync.connection.model'].search(
            [
                ('model', '=', 'product.product')
            ]
        )
        self.need_sync_connections = need_sync_connection_models.mapped('need_sync_connection')

    @api.one
    def _set_need_sync_connection(self):
        for need_sync_connection in self.need_sync_connections:
            need_sync_connection.set_published(self.id, 'product.category', need_sync_connection.published)