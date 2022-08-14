# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLocation(models.Model):

    _inherit='stock.location'

    is_contract = fields.Boolean(string="Es un contrato")
    warehouse_id = fields.Many2one('stock.warehouse', string='Almacen/Obra', required=False)

    # Establecemos el nombre de la ubiciación al cambiar el campo de warehouse
    @api.onchange('warehouse_id')
    def _onchange_warehouse(self):
        for rec in self:
            # Si hay una almacén establecido...
            if(rec.warehouse_id):
                # Agregamos el nombre del almacén al nombre de la ubicación
                rec['name'] = rec.warehouse_id.name + '/CONTRATO ' + rec['name']
                return

    def _set_is_contract(self):
        for location in self:
            if(location.location_id):
                return
            else:
                location["is_contract"] = True
                return