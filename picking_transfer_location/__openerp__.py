# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
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
    'name': 'Stock Picking Transfer Sort on Location',
    'version': '8.0.0.0.1',
    'author': 'ICTSTUDIO, André Schenkels',
    'category': 'Stock Management',
    'website': 'https://www.odoo.com',
    'depends': ['product_stock_location'],
    'demo': [],
    'summary': "Sort Transfer on Stock Location depending on Warehouse/Location",
    'data': [
        'views/stock_transfer_details.xml'
    ],
}

