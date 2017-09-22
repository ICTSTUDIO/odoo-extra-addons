# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncLine(models.Model):
    _inherit = "need.sync.line"

    @api.model
    def create(self, values):
        if values.get('res_id') and values.get('model') and values.get('need_sync_connection'):
            if values.get('model') == 'res.partner':
                nsc = self.env['need.sync.connection'].search([('id', '=', values.get('need_sync_connection'))])
                if nsc:
                    if nsc.check_unpublished(values.get('res_id'), values.get('model')):
                        values['published'] = False
                    else:
                        values['published'] = True
        return super(NeedSyncLine, self).create(values)

