# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Need Synchronization Base',
    'version': '8.0.0.0.2',
    'category': 'Stock',
    'author': 'ICTSTUDIO | André Schenkels',
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
}