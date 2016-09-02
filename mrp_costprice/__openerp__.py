# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ERP|OPEN (www.erpopen.nl).
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
{
    'name': 'MRP Costprice',
    'version': '1.0',
    'category': 'MRP',
    'description': """Update the costprice of the products with a bom""",
    'author': 'ERP|OPEN | André Schenkels',
    'website': 'http://www.erpopen.nl',
    'depends': [
        'mrp',
        'product',
    ],
    'data': [
        'view/mrp_view.xml',
    ],
}
