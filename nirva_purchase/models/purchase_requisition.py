# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseRequisition(models.Model):

    _inherit='purchase.requisition'

    @api.onchange('x_studio_obra')
    # Filtramos el dominio del campo purchase_requisition.x_subcontrato [Concepto]
    def _set_stock_location_domain(self):
        for rec in self:
            if(rec.x_studio_obra.warehouse_id):
                #Definimos el dominio
                ubicaciones_domain = [('location_id.name', "ilike", rec.x_studio_obra.warehouse_id.name)]
                return {'domain': {'x_studio_subcontrato': ubicaciones_domain}}

    def _overwrite_obra_domain(self): 
        return ["&",("code","=","incoming"),"|",("warehouse_id","!=",False),("warehouse_id.company_id","=", self.env.company.id)]

    x_studio_obra = fields.Many2one('stock.picking.type', string='Obra', domain=_overwrite_obra_domain)
    x_studio_subcontrato = fields.Many2one('stock.location', string='Concepto (Contrato/Subcontrato)', domain=[('id', '=', '-1')])

    def action_custom_rfq(self):
        for requisition in self:
            request_for_quotation = requisition.env['purchase.order'].create({
                'company_id': requisition.env.company.id,
                'currency_id': requisition.env.company.currency_id.id,
                'date_order': requisition.date_end,
                'name': 'Borrador de Solicitud de cotización',
                'picking_type_id': requisition.x_studio_obra.id,
                'state': 'draft',
                'requisition_id': requisition.id,
            })