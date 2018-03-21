# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleContractType(models.Model):
    _inherit = 'sale.order'

    contract_type = fields.Selection([
        ('axc', 'Spot'),
        ('pf', 'Precio Fijo'),
        ('pm', 'Precio Maximo'),
        ('pd', 'Precio Despues'),
	('sv', 'Servicios'),
        ('na', 'No aplica'),
    ], default='na', required=True)
