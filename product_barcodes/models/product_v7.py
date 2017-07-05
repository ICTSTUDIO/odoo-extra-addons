# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright© 2015-2017 ERP|OPEN <http://www.erpopen.nl>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from openerp.osv import orm, fields

_logger = logging.getLogger(__name__)


class ProductProduct(orm.Model):
    _inherit = 'product.product'

    # disable constraint
    def _check_ean_key(self, cr, uid, ids):
        "Inherit the method to disable the EAN13 check"
        return True
    _constraints = [(_check_ean_key, 'Error: Invalid ean code', ['ean13'])]