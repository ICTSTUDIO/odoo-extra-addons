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
    'name': 'Product Stock Location Qty',
    'version': '8.0.1.0.2',
    'website': 'http://www.ictstudio.eu',
    'category': 'Product',
    'summary': 'Show Product Qty On Stock for Location',
    'description': """
Product Stock Location Qty
===========================
- Show Product Qty On Stock for Location
""",
    'author': 'ICTSTUDIO, André Schenkels',
    'depends': ['product_stock_move_qty'],
    'data': [
        'views/stock_product_location.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'security/ir.model.access.csv',
    ],
}
