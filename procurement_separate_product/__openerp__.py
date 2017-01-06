# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Procurement Rule - Separate Product',
    'version': '8.0.0.0.2',
    'category': 'Stock',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Create a picking for each product in a procurement rule marked with option separate product',
    'depends': [
        'stock',
    ],
    'data': [
        'views/procurement_rule.xml',
    ],
}