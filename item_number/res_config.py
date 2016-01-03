# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Line Item number
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

from openerp.osv import orm, fields


class Config(orm.TransientModel):
    _inherit = 'sale.config.settings'

    _columns = {
        'module_item_number': fields.boolean(
            'Item Numbers from Sale Order Line to Invoice',
            help="""This module will allow you to maintain a correct line number for each Line."""),
    }
