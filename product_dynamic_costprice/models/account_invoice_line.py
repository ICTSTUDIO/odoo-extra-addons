# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ERP|OPEN (www.erpopen.nl).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.model
    def _anglo_saxon_sale_move_lines(self, i_line, res):
        """Return the additional move lines for sales invoices and refunds.

        i_line: An account.invoice.line object.
        res: The move line entries produced so far by the parent move_line_get.
        """
        _logger.debug("Account Anglo Saxxon Sale Move Lines")
        res = super(AccountInvoiceLine, self)._anglo_saxon_sale_move_lines(i_line, res)

        inv = i_line.invoice_id
        fiscal_pool = self.pool.get('account.fiscal.position')
        fpos = inv.fiscal_position or False
        company_currency = inv.company_id.currency_id.id

        if i_line.product_id.calc_costprice and i_line.product_id.calc_costprice_factor and i_line.product_id.type == 'consu':
            # debit account dacc will be the output account
            # first check the product, if empty check the category
            dacc = i_line.product_id.property_stock_account_output and i_line.product_id.property_stock_account_output.id
            if not dacc:
                dacc = i_line.product_id.categ_id.property_stock_account_output_categ and i_line.product_id.categ_id.property_stock_account_output_categ.id
            # in both cases the credit account cacc will be the expense account
            # first check the product, if empty check the category
            cacc = i_line.product_id.property_account_expense and i_line.product_id.property_account_expense.id
            if not cacc:
                cacc = i_line.product_id.categ_id.property_account_expense_categ and i_line.product_id.categ_id.property_account_expense_categ.id
            if dacc and cacc:
                price_unit = i_line.price_unit / i_line.product_id.calc_costprice_factor
                from_unit = i_line.product_id.uom_id.id
                to_unit = i_line.uos_id.id
                price_unit = self.env['product.uom']._compute_price(from_unit, price_unit, to_uom_id=to_unit)
                return [
                    {
                        'type':'src',
                        'name': i_line.name[:64],
                        'price_unit':price_unit,
                        'quantity':i_line.quantity,
                        'price':self._get_price(inv, company_currency, i_line, price_unit),
                        'account_id':dacc,
                        'product_id':i_line.product_id.id,
                        'uos_id':i_line.uos_id.id,
                        'account_analytic_id': False,
                        'taxes':i_line.invoice_line_tax_id,
                    },

                    {
                        'type':'src',
                        'name': i_line.name[:64],
                        'price_unit':price_unit,
                        'quantity':i_line.quantity,
                        'price': -1 * self._get_price(inv, company_currency, i_line, price_unit),
                        'account_id':fiscal_pool.map_account(self.env.cr, self.env.uid, fpos, cacc),
                        'product_id':i_line.product_id.id,
                        'uos_id':i_line.uos_id.id,
                        'account_analytic_id': False,
                        'taxes':i_line.invoice_line_tax_id,
                    },
                ]
        return res