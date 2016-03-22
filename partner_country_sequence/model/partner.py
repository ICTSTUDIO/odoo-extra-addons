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
from openerp.osv.expression import get_unaccent_wrapper

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
        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):

            self.check_access_rights(cr, uid, 'read')
            where_query = self._where_calc(cr, uid, args, context=context)
            self._apply_ir_rules(cr, uid, where_query, 'read', context=context)
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(cr)

            query = """SELECT id
                         FROM res_partner
                      {where} ({email} {operator} {percent}
                           OR {display_name} {operator} {percent} OR {ref} {operator} {percent})
                     ORDER BY {display_name}
                    """.format(where=where_str, operator=operator,
                               email=unaccent('email'),
                               display_name=unaccent('display_name'),
                               ref=unaccent('ref'),
                               percent=unaccent('%s'))

            where_clause_params += [search_name, search_name, search_name]
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            cr.execute(query, where_clause_params)
            ids = map(lambda x: x[0], cr.fetchall())

            if ids:
                return self.name_get(cr, uid, ids, context)
            else:
                return []
        return super(res_partner,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)

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
    
