# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################
#
# ChriCar Beteiligungs- und Beratungs- GmbH
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
# created 2009-09-19 23:51:03+02
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
from openerp.osv import fields,osv
from openerp.tools.sql import drop_view_if_exists

class stock_move_by_location(osv.osv):
     _name = "stock_move_by_location"
     _description = "Location Moves"
     _auto = False

     _columns = {
       'id'                 : fields.char    ('id',size=16, readonly=True),
       'description'        : fields.char    ('Description', size=16, readonly=True),
       'location_id'        : fields.many2one('stock.location','Location', select=True, readonly=True),
       'product_id'         : fields.many2one('product.product','Product', select=True, readonly=True),
       'categ_id'           : fields.related ('product_id','categ_id',type="many2one", relation="product.category", string='Category',readonly=True),
       'name'               : fields.float   ('Quantity', digits=(16,2), readonly=True),
       'uom_id'             : fields.related ('product_id', 'uom_id', type="many2one", relation="product.uom", string="UoM", readonly = True ),
       'product_qty_pending': fields.float   ('Quantity Pending', digits=(16,2), readonly=True),
       'date'               : fields.datetime('Date Planned', select=True, readonly=True),
       'picking_id'         : fields.many2one('stock.picking', 'Packing', select=True, readonly=True),
       'company_id': fields.many2one('res.company', 'Company', readonly=True),
}
     def init(self, cr):
          drop_view_if_exists(cr, 'stock_product_by_location')
          drop_view_if_exists(cr, 'stock_move_by_location')

          cr.execute("""create or replace view stock_move_by_location
as
select i.id ,
 l.id as location_id,product_id,
 i.name as description,
 case when state ='done' then product_qty else 0 end as name,
 case when state !='done' then product_qty else 0 end as product_qty_pending,
 date,
 picking_id,l.company_id
from stock_location l,
     stock_move i
where l.usage='internal'
  and i.location_dest_id = l.id
  and state != 'cancel'
  and i.company_id = l.company_id
union all
select -o.id ,
l.id as location_id ,product_id,
 o.name as description,
 case when state ='done' then -product_qty else 0 end as name,
 case when state !='done' then -product_qty else 0 end as product_qty_pending,
 date,
 picking_id,l.company_id
from stock_location l,
     stock_move o
where l.usage='internal'
  and o.location_id = l.id
  and state != 'cancel'
  and o.company_id = l.company_id
;""")

stock_move_by_location()


class stock_product_by_location(osv.osv):
     _name = "stock_product_by_location"
     _description = "Product Stock Sum"
     _auto = False

     _columns = {
       'id'                 : fields.char    ('id',size=16, readonly=True),
       'location_id'        : fields.many2one('stock.location','Location', select=True, required=True, readonly=True),
       'product_id'         : fields.many2one('product.product','Product', select=True, required=True, readonly=True),
       'uom_id'             : fields.related ('product_id', 'uom_id', type="many2one", relation="product.uom", string="UoM", readonly = True ),
       'categ_id'           : fields.related ('product_id','categ_id', type="many2one", relation="product.category", string='Category',readonly=True),
       'cost_method'        : fields.related ('product_id', 'cost_method', type="char", relation="product.product", string="Cost Method", readonly = True ),
       'name'               : fields.float   ('Quantity', digits=(16,2), readonly=True),
       'product_qty_pending': fields.float   ('Quantity Pending', digits=(16,2), readonly=True),
       'company_id': fields.many2one('res.company', 'Company', readonly=True),
}
     _defaults = {
}


     def init(self, cr):
          drop_view_if_exists(cr, 'stock_product_by_location')
     
          cr.execute("""create or replace view stock_product_by_location
as
select min(id) as id ,location_id,product_id,
       sum(name) as name, sum(product_qty_pending) as product_qty_pending, 
       company_id
 from stock_move_by_location
group by location_id,product_id,company_id
having round(sum(name),4) != 0 
;""")

stock_product_by_location()


class product_product(osv.osv):
      _inherit = "product.product"
      _columns = {
          'stock_product_by_location_ids': fields.one2many('stock_product_by_location','product_id','Product by Stock '),
      }

#copy must not copy stock_product_by_location_ids
      def copy (self, cr, uid, id, default={}, context=None):
          default = default.copy()
          default['stock_product_by_location_ids'] = []
          return super(product_product, self).copy (cr, uid, id, default, context)
      # end def copy
product_product()

class stock_location(osv.osv):
      _inherit = "stock.location"
      _columns = {
          'stock_product_by_location_ids': fields.one2many('stock_product_by_location','location_id','Product by Stock '),
      }

      def copy (self, cr, uid, id, default={}, context=None):
          default = default.copy()
          default['stock_product_by_location_ids'] = []
          return super(stock_location, self).copy (cr, uid, id, default, context)
      # end def copy

#copy must not copy stock_product_by_location_ids
stock_location()
