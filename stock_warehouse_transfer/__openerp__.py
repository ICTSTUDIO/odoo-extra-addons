# -*- encoding: utf-8 -*-
##############################################################################
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

{
    'name': 'Stock Warehouse Transfer',
    'version': '8.0.0.0.1',
    'license': 'AGPL-3',
    'author': 'ICTSTUDIO',
    'website': 'http://www.ictstudio.eu',
    'category': 'Purchase',
    'complexity': 'normal',
    'summary': 'Create a transfer of products between 2 warehouses',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_warehouse_transfer.xml',
        'data/ir_sequence.xml'
    ],
}
