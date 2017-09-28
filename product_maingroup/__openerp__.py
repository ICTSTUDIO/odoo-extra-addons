# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Product Main Group',
    'version': '8.0.0.0.1',
    'category': 'Stock',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Add Top level product group on product',
    'depends': [
        'stock',
    ],
    'data': [
        'views/product_template.xml',
        'views/product_product.xml',
        'views/product_category.xml',
    ],
}