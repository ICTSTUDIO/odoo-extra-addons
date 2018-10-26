# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'User Role and Auth OIDC - Open Connect ID Roles',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'https://www.ictstudio.eu',
    'license': 'LGPL-3',
    'depends': [
        'auth_oidc',
        'base_user_role',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/matrix_role_company.xml'
    ],
    'installable': False,
}