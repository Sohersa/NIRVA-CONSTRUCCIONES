# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLocation(models.Model):

    _inherit='stock.location'

    is_contract = fields.Boolean(string="Es un contrato")
    warehouse_id = fields.Many2one('stock.warehouse', string='Almacen/Obra', required=False)

    def _set_contract_name(rec):
        rec['name'] = rec.warehouse_id.name + '/CONTRATO ' + rec['name']
        return


    # Establecemos el nombre de la ubiciación al cambiar el campo de warehouse
    @api.onchange('warehouse_id')
    def _onchange_warehouse(self):
        for rec in self:
            # Si hay una almacén establecido...
            if(rec.warehouse_id):
                # Agregamos el nombre del almacén al nombre de la ubicación
                self._set_contract_name(rec)
                return

    def _set_is_contract(self):
        for location in self:
            if not location.location_id and location.usage == "transit":
                location["is_contract"] = True
                self._set_contract_name(location)
                return