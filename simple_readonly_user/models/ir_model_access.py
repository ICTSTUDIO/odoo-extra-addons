# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)


import logging

from odoo import api, models, tools
_logger = logging.getLogger(__name__)

class IrModelAccess(models.Model):
    _inherit = 'ir.model.access'

    @api.model
    @tools.ormcache_context('self._uid', 'model', 'mode', 'raise_exception', keys=('lang',))
    def check(self, model, mode='read', raise_exception=True):
        """
        Inherit Check method to create a Readonly User
        """
        ret = super(IrModelAccess, self).check(model, mode, raise_exception=raise_exception)
        if self.check_groups('simple_readonly_user.group_simple_readonly_user'):
            if mode != 'read':
                return False
        return ret