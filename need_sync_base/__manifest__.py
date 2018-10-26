# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Need Synchronization Base',
    'version': '10.0.0.0.7',
    'category': 'Tools',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Base module for external connections detecting changed models in ODOO',
    'depends': [
        'base',
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/need_sync.xml',
        'views/need_sync_line.xml',
        'views/need_sync_connection.xml',
        'views/need_sync_model.xml',
        'views/menu.xml',
        'data/need_sync_model.xml'
    ],
    'installable': False,
}