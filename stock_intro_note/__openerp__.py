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
    "name" : "Stock Picking Intro Notes",
    "version": "1.0",
    "category": "Sale",
    "author": "ICTSTUDIO, André Schenkels",
    'summary': 'Stock Picking Intro Note - Intro Message on Documents',
    'website': 'http://www.ictstudio.eu',
    "depends":
        [
            "stock"
        ],

    'data':
        [
            'view/stock_view.xml',
            'view/report_stock_picking.xml',
        ],
}

