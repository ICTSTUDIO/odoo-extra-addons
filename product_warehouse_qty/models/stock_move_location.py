# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
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

from openerp import models, fields
from openerp import tools

_logger = logging.getLogger(__name__)

class StockMoveLocation(models.Model):
    _name = "stock_move_location"
    _description = "Location Moves"
    _auto = False

    id = fields.Char(
            string='id',
            size=16,
            readonly=True
    )
    description = fields.Char(
            string='Description',
            size=16,
            readonly=True
    )
    location_id = fields.Many2one(
            comodel_name='stock.location',
            string='Location',
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
    uom_id = fields.Many2one (
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
    qty_processing = fields.Float(
            string='Quantity Processing',
            digits=(16,2),
            readonly=True
    )
    qty_in_transit = fields.Float(
            string='Quantity Transit',
            digits=(16,2),
            readonly=True
    )
    qty_in_transit_processing = fields.Float(
            string='Quantity Transit Processing',
            digits=(16,2),
            readonly=True
    )
    qty_backorder = fields.Float(
            string='Quantity Backorder',
            digits=(16,2),
            readonly=True
    )

    def _view_internal_add(self):
        view_str = """select sm.id ,
 sl.id as location_id,sm.product_id, sm.warehouse_id,
 sm.name as description,
 case when sm.state ='done' then sm.product_qty else 0 end as qty_on_hand,
 case when sm.state !='done' then sm.product_qty else 0 end as qty_processing,
 0 as qty_in_transit,
 0 as qty_in_transit_processing,
 0 as qty_backorder,
 sm.date,
 sm.picking_id,sl.company_id
from stock_location sl,
     stock_move sm
left join stock_picking sp ON
    sp.id = sm.picking_id
where sl.usage='internal'
  and sm.location_dest_id = sl.id
  and sm.state != 'cancel'
  and sm.company_id = sl.company_id
  and sp.backorder_id is null"""
        return view_str

    def _view_internal_deduct(self):
        view_str = """select -sm.id ,
sl.id as location_id ,sm.product_id, sm.warehouse_id,
 sm.name as description,
 case when sm.state ='done' then -sm.product_qty else 0 end as qty_on_hand,
 case when sm.state !='done' then -sm.product_qty else 0 end as qty_processing,
 0 as qty_in_transit,
 0 as qty_in_transit_processing,
 0 as qty_backorder,
 sm.date,
 sm.picking_id,sl.company_id
from stock_location sl,
     stock_move sm
left join stock_picking sp ON
    sp.id = sm.picking_id
where sl.usage='internal'
  and sm.location_id = sl.id
  and sm.state != 'cancel'
  and sm.company_id = sl.company_id
  and sp.backorder_id is null"""
        return view_str

    def _view_transit_add(self):
        view_str = """select sm.id ,
 sl.id as location_id,sm.product_id, sm.warehouse_id,
 sm.name as description,
 0 as qty_on_hand,
 0 as qty_processing,
 case when sm.state ='done' then sm.product_qty else 0 end as qty_in_transit,
 case when sm.state !='done' then sm.product_qty else 0 end as qty_in_transit_processing,
 0 as qty_backorder,
 sm.date,
 sm.picking_id,sl.company_id
from stock_location sl,
     stock_move sm
left join stock_picking sp ON
    sp.id = sm.picking_id
where sl.usage='transit'
  and sm.location_dest_id = sl.id
  and sm.state != 'cancel'
  and sm.company_id = sl.company_id
  and sp.backorder_id is null"""
        return view_str

    def _view_transit_deduct(self):
        view_str = """select -sm.id ,
sl.id as location_id ,sm.product_id, sm.warehouse_id,
 sm.name as description,
 0 as qty_on_hand,
 0 as qty_processing,
 case when sm.state ='done' then -sm.product_qty else 0 end as qty_in_transit,
 case when sm.state !='done' then -sm.product_qty else 0 end as qty_in_transit_processing,
 0 as qty_backorder,
 sm.date,
 sm.picking_id,sl.company_id
from stock_location sl,
     stock_move sm
left join stock_picking sp ON
    sp.id = sm.picking_id
where sl.usage='transit'
  and sm.location_id = sl.id
  and sm.state != 'cancel'
  and sm.company_id = sl.company_id
  and sp.backorder_id is null"""
        return view_str

    def _view_backorder_add(self):
        view_str = """select sm.id ,
 sl.id as location_id,sm.product_id, sm.warehouse_id,
 sm.name as description,
 0 as qty_on_hand,
 0 as qty_processing,
 0 as qty_in_transit,
 0 as qty_in_transit_processing,
 sm.product_qty as qty_backorder,
 sm.date,
 sm.picking_id,sl.company_id
from stock_location sl,
     stock_move sm
left join stock_picking sp ON
    sp.id = sm.picking_id
where sl.usage='internal'
  and sm.location_dest_id = sl.id
  and sm.state not in ('cancel','done')
  and sm.company_id = sl.company_id
  and sp.backorder_id is not null"""
        return view_str

    def _view_backorder_deduct(self):
        view_str = """select -sm.id ,
sl.id as location_id ,sm.product_id, sm.warehouse_id,
 sm.name as description,
 0 as qty_on_hand,
 0 as qty_processing,
 0 as qty_in_transit,
 0 as qty_in_transit_processing,
 -sm.product_qty as qty_backorder,
 sm.date,
 sm.picking_id,sl.company_id
from stock_location sl,
     stock_move sm
left join stock_picking sp ON
    sp.id = sm.picking_id
where sl.usage='internal'
  and sm.location_id = sl.id
  and sm.state not in ('cancel','done')
  and sm.company_id = sl.company_id
  and sp.backorder_id is not null"""
        return view_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute(
                """CREATE or REPLACE VIEW %s as (
            %s
            union all
            %s
            union all
            %s
            union all
            %s
            union all
            %s
            union all
            %s
            )""" % (self._table,
                    self._view_internal_add(),
                    self._view_internal_deduct(),
                    self._view_backorder_add(),
                    self._view_backorder_deduct(),
                    self._view_transit_add(),
                    self._view_transit_deduct(),
                    )
        )
