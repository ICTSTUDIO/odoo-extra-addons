# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from odoo import models, fields
from odoo import tools

_logger = logging.getLogger(__name__)

class StockMoveLocation(models.Model):
    _name = "stock.move.location"
    _description = "Location Moves"
    _auto = False
    _order = "date desc, location_name"

    id = fields.Char(
            string='id',
            size=16,
            readonly=True
    )
    description = fields.Char(
            string='Description',
            readonly=True
    )
    location_id = fields.Many2one(
            comodel_name='stock.location',
            string='Location',
            readonly=True
    )
    location_name = fields.Char(
            string='Location Full Name',
            readonly=True
    )
    product_id = fields.Many2one(
            comodel_name='product.product',
            string='Product',
            readonly=True
    )
    product_tmpl_id = fields.Many2one(
            related='product_id.product_tmpl_id',
            comodel_name='product.template',
            string='Product Template'
    )
    categ_id = fields.Many2one(
            related='product_id.categ_id',
            comodel_name="product.category",
            string='Category',
            readonly=True
    )
    uom_id = fields.Many2one(
            related='product_id.uom_id',
            comodel_name="product.uom",
            string="UoM",
            readonly = True
    )
    date = fields.Datetime(
            string='Date Planned',
            readonly=True
    )
    picking_id = fields.Many2one(
            comodel_name='stock.picking',
            string='Packing',
            readonly=True
    )
    company_id = fields.Many2one(
            comodel_name='res.company',
            string='Company',
            readonly=True
    )
    warehouse_id = fields.Many2one(
            comodel_name='stock.warehouse',
            string='Warehouse',
            readonly=True
    )
    qty_on_hand = fields.Float(
            string='Quantity',
            digits=(16,2),
            readonly=True
    )
    qty_incoming = fields.Float(
            string='Incoming',
            digits=(16,2),
            readonly=True
    )
    qty_outgoing = fields.Float(
            string='Outgoing',
            digits=(16,2),
            readonly=True
    )
    qty_internal = fields.Float(
            string='Internal',
            digits=(16,2),
            readonly=True
    )
    qty_manual = fields.Float(
            string='Manual',
            digits=(16,2),
            readonly=True
    )
    move_type = fields.Char(
            string='Move Type',
            readonly=True
    )



    def _view_internal_add(self):
        view_str = """select sm.id ,
 sl.id as location_id,sm.product_id, sm.warehouse_id,
 sm.name as description,
 case when sm.state ='done' then sm.product_qty else 0 end as qty_on_hand,
 case when sm.state != 'done' and spt.code = 'internal' then sm.product_qty else 0 end as qty_internal,
 case when sm.state != 'done' and spt.code = 'incoming' then sm.product_qty else 0 end as qty_incoming,
 case when sm.state != 'done' and spt.code = 'outgoing' then sm.product_qty else 0 end as qty_outgoing,
 case when sm.state != 'done' and sm.picking_type_id = NULL then sm.product_qty else 0 end as qty_manual,
 sm.date,
 sm.picking_id,sl.company_id,
 sl.complete_name as location_name,
 spt.code as move_type
from
     stock_move sm
     left join stock_location sl ON
        sm.location_dest_id = sl.id
    left join stock_picking sp ON
        sp.id = sm.picking_id
     left join stock_picking_type spt ON
        sp.picking_type_id = spt.id
where sl.usage='internal'
  and sm.state != 'cancel'
  and sm.company_id = sl.company_id
  """
        return view_str

    def _view_internal_deduct(self):
        view_str = """select -sm.id ,
sl.id as location_id ,sm.product_id, sm.warehouse_id,
 sm.name as description,
 case when sm.state ='done' then -sm.product_qty else 0 end as qty_on_hand,
 case when sm.state != 'done' and spt.code = 'internal' then -sm.product_qty else 0 end as qty_internal,
 case when sm.state != 'done' and spt.code = 'incoming' then -sm.product_qty else 0 end as qty_incoming,
 case when sm.state != 'done' and spt.code = 'outgoing' then -sm.product_qty else 0 end as qty_outgoing,
 case when sm.state != 'done' and sm.picking_type_id = NULL then -sm.product_qty else 0 end as qty_manual,
 sm.date,
 sm.picking_id,sl.company_id,
 sl.complete_name as location_name,
 spt.code as move_type
from
     stock_move sm
     left join stock_location sl ON
     sm.location_id = sl.id
     left join stock_picking sp ON
        sp.id = sm.picking_id
     left join stock_picking_type spt ON
        sp.picking_type_id = spt.id

where sl.usage='internal'
  and sm.state != 'cancel'
  and sm.company_id = sl.company_id
  """
        return view_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        sql ="""CREATE or REPLACE VIEW %s as (
            %s
            union all
            %s
            )""" % (self._table,
                    self._view_internal_add(),
                    self._view_internal_deduct()
                    )
        self.env.cr.execute(sql)