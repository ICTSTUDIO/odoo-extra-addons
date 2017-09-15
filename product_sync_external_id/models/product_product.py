# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import re
import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _filter_default_code(self, code):
        """
        Removes unwanted characters from the product default_code
        :param code: default_code
        :return: filtered code
        """
        new_code = False
        if code:
            _logger.debug('Default Code: %s', code)
            new_code = re.sub("[/.,()-]", "__", code)
            _logger.debug('New Code: %s', new_code)
        return new_code

    @api.multi
    def set_all_external_ids(self):
        all_products = self.search([])
        if all_products:
            all_products._set_external_id()
        return True

    @api.multi
    def _set_external_id(self):
        model_env = self.env['ir.model.data']
        for product in self:
            default_code = self._filter_default_code(product.default_code)

            model_searchs = model_env.search(
                    [
                        ('res_id', '=', product.id),
                        ('model', '=', 'product.product'),
                    ]
            )
            model_checks = model_env.search(
                    [
                        ('name', '=', default_code),
                        ('module', '=', '__product__')
                    ]
            )

            _logger.debug("Checks: %s", model_checks)
            _logger.debug("Searchs: %s", model_searchs)

            if not model_checks:
                check_code = default_code
            else:
                check_code = False

            external_values = {
                'noupdate': False,
                'name': check_code or ('product_product_%s' % product.id),
                'res_id': product.id,
                'model': 'product.product',
                'module': '__product__'
            }

            _logger.debug("Set External Values: %s", external_values)
            if model_searchs and check_code:
                _logger.debug("Update External Values: %s", external_values)
                model_searchs.write(external_values)
            elif check_code:
                _logger.debug("Create new external id: %s", external_values)
                model_env.create(external_values)
            else:
                _logger.debug("Nothing to do")

            for template in product.product_tmpl_id:
                tmpl_model_searchs = model_env.search(
                        [
                            ('res_id', '=', template.id),
                            ('model', '=', 'product.template'),
                        ]
                )
                tmpl_model_checks = model_env.search(
                        [
                            ('name', '=', default_code),
                            ('module', '=', '__template__')
                        ]
                )

                if not tmpl_model_checks:
                    check_code = default_code
                else:
                    check_code = False

                tmpl_external_values = {
                    'noupdate': False,
                    'name': check_code or ('product_template_%s' % template.id),
                    'res_id': template.id,
                    'model': 'product.template',
                    'module': '__template__'
                }

                _logger.debug("Set External Values: %s", tmpl_external_values)
                if tmpl_model_searchs and check_code:
                    _logger.debug("Write External Values: %s", tmpl_external_values)
                    tmpl_model_searchs.write(tmpl_external_values)
                elif check_code:
                    _logger.debug("Create External Values: %s", tmpl_external_values)
                    model_env.create(tmpl_external_values)