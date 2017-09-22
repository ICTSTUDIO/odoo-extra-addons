# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncConnectionRecordException(models.Model):
    _inherit = "need.sync.connection.record.exception"
    _description = "Need Sync Connection Records Not synced"


    def _select_models(self):
        list_models = super(NeedSyncConnectionRecordException, self)._select_models()
        list_models.append(('product.category', 'Product Category'))
        return list_models

    model = fields.Selection(
        selection=_select_models,
    )

    record = fields.Reference(
        selection=_select_models,
    )

    @api.model
    def get_need_sync_lines(self, res_ids, model, connection_id):
        if isinstance(res_ids, (long, int)):
            res_ids = [res_ids]
        need_sync_lines = super(NeedSyncConnectionRecordException, self).get_need_sync_lines(
            res_ids, model, connection_id
        )
        if model == 'product.category':
            products = self.env['product.product'].search(
                [
                    ('categ_id', 'in', res_ids)
                ]
            )
            if products:
                product_res_ids = list(set(
                    products.ids) - set(
                    self.get_exceptions_res_ids('product.product', connection_id)))
                need_sync_lines = need_sync_lines | self.get_need_sync_lines(
                    product_res_ids,
                    'product.product',
                    connection_id
                )

        return need_sync_lines

    @api.model
    def get_exceptions_res_ids(self, model, connection_id):
        exceptions = self.search(
            [
                ('model', '=', model),
                ('need_sync_connection', '=', connection_id)
            ]
        )
        return_list = []
        for x in exceptions:
            return_list.append(x.res_id)
        return return_list