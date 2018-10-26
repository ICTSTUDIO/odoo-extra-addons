# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Product Marker',
    'version': '10.0.1.0.1',
    'category': 'Product',
    'summary': 'Provide Markers on Products',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'depends': ['product', 'stock'],
    'data': [
        'security/product_marker_security.xml',
        'views/product_marker.xml',
        'views/product_template.xml',
        'views/product_product.xml',
        'security/ir.model.access.csv',
    ],
    'installable': False,
}

