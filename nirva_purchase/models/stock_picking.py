# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):

    _inherit='stock.picking'

    # Filtramos el dominio del campo purchase_order
    # def _set_purchase_order(self):
    #     domain =[('id', '=', -1)]
    #     purchase_order_list=[]
    #     purchase_orders = self.env['purchase.order'].search([('name','=', self.origin)])
    #     for each in purchase_orders:
    #         purchase_order_list.append(each.id)
    #     if purchase_order_list:
    #         domain =[('id', 'in', purchase_order_list)]
    #         return domain
    #     return domain

    # Agregamos un campo relacional para poder acceder a la orden
    # de compra de la cuál deriva la recepción de los productos
    purchase_order = fields.Many2one('purchase.order', string='Orden de compra')

    @api.onchange('name')
    def _set_purchase_order_domain(self):
        for rec in self:
            # Definimos el dominio
            purchase_order_domain = [["name","=", rec.origin]]
            return {'domain': {'purchase_order': purchase_order_domain}}