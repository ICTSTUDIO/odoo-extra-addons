# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncConnectionModel(models.Model):
    _name = "need.sync.connection.model"
    _description = "Need Sync Connection Models"
    _rec_name = 'model'

    def _select_models(self):
        return self.env['need.sync.model']._select_models()

    model = fields.Selection(
            selection=_select_models,
            string="Model",
            required=True,
            index=True
    )
    need_sync_connection = fields.Many2one(
            comodel_name="need.sync.connection",
            string="Connection",
            index=True
    )
    auto_create_lines = fields.Boolean(
            string="Create Sync Lines Automatic",
            default=False,
            help="Create a sync line for every product available automatically"
    )

    _sql_constraints = {
        (
            'connection_model_uniq',
            'unique(model, need_sync_connection)',
            'Only one model per connection'
        )
    }
