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
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp.osv.expression import get_unaccent_wrapper

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char(
            string="Reference",
            required=True,
            default='[Auto]'
    )

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        for rec in self:
            if rec.parent_id:
                if rec.ref != rec.parent_id.ref:
                    rec.ref = rec.parent_id.ref
            elif rec.child_ids:
                for child in rec.child_ids:
                    if child.ref != rec.ref:
                        child.ref = rec.ref
        return res

    @api.one
    @api.constrains('ref', 'parent_id')
    def _check_ref(self):
        if not self.parent_id:
            # Search with in active partners
            found_partners = self.with_context({'active_test': False}).search(
                    [
                        ('ref', '=', self.ref),
                        ('parent_id', '=', False)
                    ]
            )
            if found_partners and not self.parent_id:
                if len(found_partners) > 1:
                    # If more then one partner with ref raise error
                    raise ValidationError("Partner with Ref already exists")

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

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
            self.env.cr.execute(query, where_clause_params)
            ids = map(lambda x: x[0], self.env.cr.fetchall())

            if ids:
                return self.browse(ids).name_get()
            else:
                return []
        return super(ResPartner, self).name_search(
                name, args, operator=operator, limit=limit
        )

    @api.model
    def create(self, vals):
        # Check if sequence exists for specific country, and get a new number
        if vals.get('ref', '[Auto]') == '[Auto]' and not vals.get('parent_id'):
            if 'country_id' in vals:
                partner_sequence = self.env['res.partner.sequence'].search(
                        [
                            ('country_id', '=', vals['country_id'])
                        ]
                )
                if partner_sequence and partner_sequence.sequence_id:
                    while True:
                        vals['ref'] = partner_sequence.sequence_id.next_by_id()
                        if self.with_context({'active_test': False}).search(
                                [
                                    ('ref', '=', vals['ref'])
                                ]
                        ):
                            _logger.debug("Partner Ref already exists in database")
                        else:
                            break

        # If no number was found with the specific country approach the default sequence will be used
        if vals.get('ref', '[Auto]') == '[Auto]' and not vals.get('parent_id'):
             while True:
                vals['ref'] = self.env['ir.sequence'].next_by_code('res.partner')
                if self.with_context({'active_test': False}).search(
                        [
                            ('ref', '=', vals['ref'])
                        ]
                ):
                    _logger.debug("Partner Ref already exists in database")
                else:
                    break

        ## If no sequence was found
        if vals.get('ref', '[Auto]') == '[Auto]' and not vals.get('parent_id'):
            raise ValidationError("No partner sequence is defined")

        if vals.get('parent_id') and vals.get('ref'):
            parent = self.browse(vals.get('parent_id'))
            vals['ref'] = parent.ref

        return super(ResPartner, self).create(vals)
    

