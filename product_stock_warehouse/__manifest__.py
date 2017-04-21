# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Products Stock Warehouse',
    'version': '10.0.0.0.2',
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'complexity': 'normal',
    'summary': "Show Stock Available each Warehouse",
    'category': 'Stock Management',
    'website': 'https://www.odoo.com',
    'depends': [
        'stock'
    ],
    'demo': [],
    'data': [
        'views/stock_warehouse.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'wizard/warehouse_change_product_qty.xml'
    ],
    'installable': True,
}

