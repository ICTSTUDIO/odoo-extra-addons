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

import logging
from openerp.osv import osv, fields
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class res_partner_sequence(osv.osv):
    _name = 'res.partner.sequence'

    _columns = {
        'country_id': fields.many2one('res.country', 'Country', required=True),
        'sequence_id': fields.many2one('ir.sequence', 'Sequence', required=True)
        }

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def _check_ref(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        else:
            context = context.copy()
        context.update({'active_test': False})
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.is_company and partner.ref:
                list_partner_ids = self.search(cr,uid,[('ref','=',partner.ref)])
                if self.search(cr,uid,[('ref','=',partner.ref)]):
                    if len(list_partner_ids)==1 and partner.id == list_partner_ids[0]:
                        return True
                    return False
        return True
    
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if context is None:
            context = {}
        else:
            context = context.copy()

        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]
            query_args = {'name': search_name, 'ref': search_name}
            query = ('''SELECT partner.id FROM res_partner partner
                                          LEFT JOIN res_partner company
                                               ON partner.parent_id = company.id
                        WHERE partner.email ''' + operator +''' %(name)s OR partner.ref ''' + operator +''' %(ref)s OR
                              CASE
                                   WHEN company.id IS NULL OR partner.is_company
                                       THEN '[' || partner.ref || '] ' || partner.name
                                   ELSE company.name || ', ' || '[' || partner.ref || '] ' || partner.name
                              END ''' + operator + ''' %(name)s
                        ORDER BY
                              CASE
                                   WHEN company.id IS NULL OR partner.is_company
                                       THEN partner.name
                                   ELSE company.name || ', ' || partner.name
                              END''')
            if limit:
                query += ' limit %(limit)s'
                query_args['limit'] = limit
            cr.execute(query, query_args)
            ids = map(lambda x: x[0], cr.fetchall())
            ids = self.search(cr, uid, [('id', 'in', ids)] + args, limit=limit, context=context)
            if ids:
                return self.name_get(cr, uid, ids, context)
        return super(res_partner,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)

    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        else:
            context = context.copy()

        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        def _name_get(d):
            name = d.get('name', '')
            code = d.get('ref', False)
            city = d.get('city', '')
            if code:
                name = '[%s] %s' % (code, name)
            return (d['id'], name)

        result = []

        for partner in self.browse(cr, user, ids, context=context):
            mydict = {
                          'id': partner.id,
                          'name': partner.name,
                          'ref': partner.ref,
                          'city': partner.city,
                          'type': partner.type
                          }
            result.append(_name_get(mydict))
        return result
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        else:
            context = context.copy()

        context.update({'active_test': False})

        # Check if sequence exists for specific country, and get a new number
        if vals.get('ref', '[Auto]') == '[Auto]':
            if 'country_id' in vals:
                partner_sequence_id = self.pool.get('res.partner.sequence').search(cr, uid,[('country_id','=',vals['country_id'])])
                if partner_sequence_id:
                    sequence_ids = self.pool.get('res.partner.sequence').read(cr, uid,[partner_sequence_id[0]],['sequence_id'])
                    if sequence_ids:
                        while True:
                            vals['ref'] = self.pool.get('ir.sequence').next_by_id(cr, uid, sequence_ids[0]['sequence_id'][0])
                            if self.search(cr,uid,[('ref','=',vals['ref'])],context=context):
                                _logger.debug("partner get next by code res.partner code already exists in database")
                            else:
                                break
        # If no number was found with the specific country approach the default sequence will be used
        if vals.get('ref', '[Auto]') == '[Auto]':
             while True:
                vals['ref'] = self.pool.get('ir.sequence').next_by_code(cr, uid, 'res.partner', context=context)
                if self.search(cr,uid,[('ref','=',vals['ref'])],context=context):
                    _logger.debug("partner get next by code res.partner code already exists in database")
                else:
                    break

        ## If no sequence was found
        if vals.get('ref', '[Auto]') == '[Auto]':
             raise osv.except_osv(
                 _('Error !'),
                 _('No partner sequence is defined'))

        return super(res_partner, self).create(cr, uid, vals, context)
    
    _columns = {
        'ref': fields.char("Reference", required=True),
        }

    _defaults = {
        'ref': '[Auto]',
        }

    _constraints = [
        (_check_ref, 'A customer number can only be used once', ['ref'])
        ]
    
