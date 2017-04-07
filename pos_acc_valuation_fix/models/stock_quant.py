# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp.osv import fields, osv, orm
import logging
_logger = logging.getLogger(__name__)


class stock_quant(osv.osv):
    _inherit = "stock.quant"

    def _get_accounting_data_for_valuation(self, cr, uid, move, context=None):
        """
        Return the accounts and journal to use to post Journal Entries for the real-time
        valuation of the move.

        :param context: context dictionary that can explicitly mention the company to consider via the 'force_company' key
        :raise: osv.except_osv() is any mandatory account or journal is not defined.
        """

        journal_id, acc_src, acc_dest, acc_valuation = super(stock_quant, self)._get_accounting_data_for_valuation(cr, uid, move, context=context)

        _logger.debug('Accounting Valuation')
        _logger.debug('Journal: %s', journal_id)
        _logger.debug('Acc Src: %s', acc_src)
        _logger.debug('Acc Dest: %s', acc_dest)
        _logger.debug('Acc Valuation: %s', acc_valuation)

        if move.picking_id and move.picking_id.picking_type_code == 'outgoing' and not move.picking_id.partner_id and move.product_id:

            cost_acc = move.product_id.product_tmpl_id.property_account_expense and move.product_id.product_tmpl_id.property_account_expense.id or False
            if not cost_acc:
                cost_acc = move.product_id.product_tmpl_id.categ_id.property_account_expense_categ and move.product_id.product_tmpl_id.categ_id.property_account_expense_categ.id or False
            if cost_acc:
                acc_src = cost_acc
                acc_dest = cost_acc
            _logger.debug('Cost Acc: %s', cost_acc)

        return journal_id, acc_src, acc_dest, acc_valuation
