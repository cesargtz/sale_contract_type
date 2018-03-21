# -*- coding: utf-8 -*-
from openerp import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    contract_type = fields.Selection(related="order_id.contract_type", store=True, readonly=True)
