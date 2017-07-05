# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright© 2015-2017 ERP|OPEN <http://www.erpopen.nl>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Product Barcodes',
    'version': '8.0.0.1.0',
    'category': 'BBA',
    'author': 'ERP|OPEN, ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Barcodes on Products',
    'depends': [
        'base',
        'product',
        ],
    'data': [
        'views/product_product.xml',
        'views/product_template.xml',
        'security/ir.model.access.csv'
        ],
}

