# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):

    _inherit='stock.picking'

    # Agregamos un campo relacional para poder acceder a la orden
    # de compra de la cuál deriva la recepción de los productos
    purchase_order = fields.Many2one('purchase.order', string='Orden de compra')

    # Vinculamos la orden de compra al recibo en función a campo relacional
    @api.onchange('origin')
    # Filtramos el dominio del campo purchase_order
    def _set_purchase_order(self):
        for rec in self:
            #Definimos el dominio acotándolo sólo al que coincida con el nombre de origen
            purchase_order_by_name = [('name', "=", rec.origin)]
            return {'domain': {'purchase_order': purchase_order_by_name}}