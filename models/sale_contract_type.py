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

    tons = fields.Float(compute="_compute_tons" , store=False, string="Tons Contratadas")
    tons_sent = fields.Float(compute="_compute_tons_sent", store=False, string="Tons Enviadas")
    tons_invoiced = fields.Float(compute="_compute_tons_invoiced", store=False, string="Tons Facturadas")
    tons_priced = fields.Float(compute="_compute_priced" , store=False, string="Tons Preciadas")


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
        invoice_id = self.env['account.invoice'].search([('origin', '=', self.name)])
        for inv in invoice_id:
            if inv.state in ['open','paid']:
                if inv.invoice_line_ids.product_id == self.order_line.product_id:
                    self.tons_invoiced += inv.invoice_line_ids.quantity

    @api.one
    def _compute_priced(self):
        price_id = self.env['pinup.price.sale'].search([('sale_order_id', '=', self.name)])
        for pr in price_id:
            if pr.state == 'close':
                self.tons_priced += pr.pinup_tons
