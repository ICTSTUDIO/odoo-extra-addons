# -*- coding: utf-8 -*-
# Copyright© 2017-today ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
{
    'name': 'Product Labels',
    'version': '10.0.0.0.1',
    'category': 'Stock',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'LGPL-3',
    'summary': 'Print Labels on Products',
    'depends': [
        'stock',
    ],
    'data': [
        'report/report_product_labels.xml',
        'report/report_product_labels_wizard.xml',
        'views/product_template.xml',
        'wizard/product_product_label_print.xml'
    ],
}