# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseRequisition(models.Model):

    _inherit='purchase.requisition'

    @api.onchange('x_studio_obra')
    # Filtramos el dominio del campo purchase_requisition.x_subcontrato [Concepto]
    def _set_stock_location_domain(self):
        for rec in self:
            #Definimos el dominio
            ubicaciones_domain = [('location_id.name', "ilike", rec.x_studio_obra.wharehouse_id.name)]
            return {'domain': {'x_subcontrato': ubicaciones_domain}}

    def _overwrite_obra_domain(self): 
        return ["&",("code","=","incoming"),"|",("warehouse_id","!=",False),("warehouse_id.company_id","=", self.env.company.id)]

    x_studio_obra = fields.Many2one('stock.picking.type', string='Obra actualizadaaaa', domain=_overwrite_obra_domain)
    x_subcontrato = fields.Many2one('stock.location', string='Concepto actualizadooo', domain=[])


    # def _on_obra_change(self):
    # _set_picking_type_domain()
