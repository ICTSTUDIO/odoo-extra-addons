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
    'name': 'Stock Inventory for specific Supplier',
    'version': '8.0.1.0.0',
    'website': 'http://www.ictstudio.eu',
    'category': 'Product',
    'summary': 'Provide Stock inventory for one specific supplier',
    'description': """
Stock Inventory Supplier
========================
- On the stock inventory form make the supplier selectable
""",
    'author': 'ICTSTUDIO, André Schenkels',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_inventory.xml',
    ],
}

