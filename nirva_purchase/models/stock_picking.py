# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):

    _inherit='stock.picking'

    # # Agregamos un campo relacional para poder acceder a la orden
    # # de compra de la cuál deriva la recepción de los productos
    # purchase_order = fields.Many2one('purchase.order', string='Orden de compra', default=)

    # @api.onchange('origin')
    # def _set_purchase_order_domain(self):
    #     for rec in self:
    #         # Definimos el dominio
    #         purchase_order_domain = [("name","=", rec.origin)]
    #         return {'domain': {'purchase_order': purchase_order_domain}}

    # @api.model
    # def _set_purchase_order_domain(self):
    #         # Definimos el dominio
    #         return [("name","=", self.origin)]

    # @api.model
    # def _default_purchase_order(self):
    #     instance = self.env['purchase.order'].search([('name', '=', 'origin')], limit=1)
    #     return instance.id

    @api.model
    def _default_purchase_order(self):
        return self.env['purchase.order'].search([('name', '=', self.origin)], limit=1)

    purchase_order = fields.Many2one('purchase.order', string="Orden de compra", default=_default_purchase_order, required=True)

