# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class IrCronLog(models.Model):
    _name = "ir.cron.log"
    _description = "Cron logging"

