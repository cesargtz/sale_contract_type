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

    tons = fields.Float(compute="_compute_tons" , store=False, string="Toneladas Contratadas")
    tons_sent = fields.Float(compute="_compute_tons_sent", store=False, string="Toneladas Enviadas")
    tons_invoiced = fields.Float(compute="_compute_tons_invoiced", store=False, string="Toneladas Facturadas")


    @api.one
    @api.depends('order_line')
    def _compute_tons(self):
        self.tons = 0
        for line in self.order_line:
            self.tons = line.product_uom_qty
            break

    @api.one
    def _compute_tons_sent(self):
        tons_truck, tons_wagon = 0, 0
        for tons in self.env['truck.outlet'].search([('contract_id', '=', self.name), ('state', '=', 'done')]):
            if tons.stock_picking_id:
                tons_truck += tons.raw_kilos / 1000
        for tons in self.env['wagon.outlet'].search([('contract_id', '=', self.name), ('state', '=', 'done')]):
            if tons.stock_picking_id:
                tons_wagon += tons.raw_kilos / 1000
        self.tons_sent = tons_truck + tons_wagon

    @api.one
    def _compute_tons_invoiced(self):
        invoice_line = self.env['account.invoice.line'].search([('origin', '=', self.name)])
        for ivl in invoice_line:
            if ivl.product_id == self.order_line.product_id:
                self.tons_invoiced += ivl.quantity
