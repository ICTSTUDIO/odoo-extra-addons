# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime
import openerp.addons.decimal_precision as dp

class pos_config(osv.osv):
    _inherit = 'pos.config'

    _columns = {
        'direct_delivery': fields.boolean('Force Direct Delivery'),
    }

    _defaults = {
        'direct_delivery': 1,
    }