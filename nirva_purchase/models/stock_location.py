# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockLocation(models.Model):

    _inherit='stock.location'

    account_analytic_group = fields.Many2one(comodel_name="account.analytic.group", string="Grupo analítico")
    is_contract = fields.Boolean(string="Es un contrato")
    warehouse_id = fields.Many2one('stock.warehouse', string='Almacen/Obra', required=False)

    def _set_is_contract(self):
        for location in self:
            if not location.location_id and location.usage == "transit":
                location["is_contract"] = True