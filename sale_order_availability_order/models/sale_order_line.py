# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    

    def _onchange_product_id_check_availability(self):
        ret = super(SaleOrderLine, self)._onchange_product_id_check_availability()
        _logger.debug("Normal Return: %s", ret)
        return {}
