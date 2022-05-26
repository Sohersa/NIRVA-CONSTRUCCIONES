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
                'name': 'Borrador de RFQ',
                'picking_type_id': requisition.x_studio_obra.id,
                'state': 'draft',
                'requisition_id': requisition.id,
            })

            for purchase_requisition_line in requisition.line_ids:
                purchase_order_line = request_for_quotation.env['purchase.order.line'].create({
                    'name': purchase_requisition_line.product_id.name,
                    'order_id': request_for_quotation.id,
                    'price_unit': 0,
                    'product_qty': purchase_requisition_line.product_qty,
                    'product_id': purchase_requisition_line.product_id.id
                })

            # Get the client id from transport form
            request_for_quotation_id = request_for_quotation.id
                
            #Initialize required parameters for opening the form view of invoice
            #Get the view ref. by paasing module & name of the required form
            view_ref = self.env['ir.model.data'].get_object_reference('purchase', 'purchase_order_form')
            view_id = view_ref[1] if view_ref else False

            #Let's prepare a dictionary with all necessary info to open create invoice form with          
            #customer/client pre-selected
            res = {
                'type': 'ir.actions.act_window',
                'name': ('Solicitud de cotización'),
                'res_model': 'purchase.order',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'current',
                'purchase_order_id': request_for_quotation_id
            }

            return res