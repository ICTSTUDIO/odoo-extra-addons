# -*- encoding: utf-8 -*-
##############################################################################
#
#    Nato Stock Number
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class procurement_order(models.Model):
    _inherit = "procurement.order"

    nsn = fields.Char(string='NSN')

    def _run_move_create(self, cr, uid, procurement, context=None):
        vals = super(procurement_order, self)._run_move_create(cr, uid, procurement, context=context)
        vals['nsn'] = procurement.nsn
        return vals