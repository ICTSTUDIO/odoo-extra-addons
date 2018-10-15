# -*- coding: utf-8 -*-
# Copyright© 2017-today ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
{
    'name': 'Product Labels on Picking',
    'version': '10.0.0.0.1',
    'category': 'Stock',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'LGPL-3',
    'summary': 'Print Labels for Products with no barcode on incoming or outging shipment',
    'depends': [
        'stock',
        'product_labels'
    ],
    'data': [
        'views/product_template.xml',
        'wizard/product_product_label_print.xml'
    ],
}