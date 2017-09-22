# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncConnection(models.Model):
    _inherit = "need.sync.connection"

    @api.model
    def check_res_model(self, res_id, model):
        res_id, model = super(NeedSyncConnection, self).check_res_model(res_id, model)
        if model == 'product.template':
            template = self.env['product.template'].search([('id', '=', res_id)])
            if template:
                res_id = template[0].product_variant_ids[0].id
                model = 'product.product'
        return res_id, model

    @api.model
    def check_unpublished(self, res_id, model):
        return_value = super(NeedSyncConnection, self).check_unpublished(res_id, model)
        if not return_value and model == 'product.product':
            product = self.env['product.product'].search(
                [
                    ('id', '=', res_id)
                ]
            )
            if product:
                product_category_id = product.categ_id.id
                if self.check_unpublished(product_category_id, 'product.category'):
                    return_value = True

        return return_value

    @api.model
    def get_dest_model(self, active_model):
        return_value = super(NeedSyncConnection, self).get_dest_model(active_model)
        if active_model == 'product.template':
            return_value = 'product.product'
        return return_value