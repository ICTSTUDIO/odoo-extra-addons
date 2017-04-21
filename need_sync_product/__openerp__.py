# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Need Synchronization Product Module',
    'version': '9.0.0.0.4',
    'category': 'Stock',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Product Specific module for seting need sync',
    'depends': [
        'need_sync_base',
        'stock',
    ],
    'data': [
        'views/product_template.xml'
    ],
}