# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Dropshipment Address',
    'version': '10.0.0.0.1',
    'category': 'Stock',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Provide a seperate object to store dropshipment addresses',
    'depends': [
        'sale_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/stock_picking.xml',
    ],
    'installable': False,
}