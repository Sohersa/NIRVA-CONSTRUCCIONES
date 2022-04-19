# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseRequisition(models.Model):

    _inherit='purchase.requisition'

    # Limitamos el dominio del campo purchase_requisition.x_studio_obra [Obra]
    @api.onchange('x_studio_obra')
    def _set_picking_type_domain(self):
        for rec in self:
            # Definimos el dominio
            obra_domain = ["&",("code","=","incoming"),"|",("warehouse_id","!=",False),("warehouse_id.company_id","=", rec.env.company.id)]
            return {'domain': {'x_studio_obra': obra_domain}}

    # Filtramos el dominio del campo purchase_requisition.x_subcontrato [Concepto]
    @api.onchange('x_subcontrato')
    def _set_stock_location_domain(self):
        for rec in self:
            #Definimos el dominio
            ubicaciones_domain = [('location_id.name', "ilike", rec.x_studio_obra.wharehouse_id.name)]
            return {'domain': {'x_subcontrato': ubicaciones_domain}}