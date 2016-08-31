# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    #def run_scheduler(self, cr, uid, use_new_cursor=False, company_id = False, context=None):


    @api.model
    def run_scheduler(self, use_new_cursor=False, company_id=False):
        return super(ProcurementOrder, self.with_context(
                {'no_assign_manual': True})).run_scheduler(
                use_new_cursor=use_new_cursor,
                company_id=company_id
        )
