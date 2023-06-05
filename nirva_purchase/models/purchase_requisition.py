# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseRequisition(models.Model):

    _inherit='purchase.requisition'

    # Creamos el campo de las personas que pueden autorizar
    autoriza = fields.Many2one("hr.employee", string="Autorizado por", domain=[('x_studio_autoriza', '!=', False)], tracking=True)

    x_studio_referencia = fields.Char(string="Referencia interna (Requisición)")

    @api.onchange('x_studio_obra')
    # Creamos la referencia interna de la requisición
    def _set_referencia(self):
        for req in self:
            if req.x_studio_obra.warehouse_id.name:
                # Extraemos el nombre del almacén relacionado
                name = req.x_studio_obra.warehouse_id.name
                # Descomponemos el nombre en un arrar de palabras
                name_words = name.split(' ')
                # Generamos el prefijo con la última palabra
                prefix = name_words[-1][0:5].upper()
                process = "REQ"
                ref_int = prefix + "-"+ process + "-" + req.name
                req['x_studio_referencia'] = ref_int

    @api.onchange('x_studio_obra')
    # Filtramos el dominio del campo purchase_requisition.x_studio_subcontrato [Concepto]
    def _set_stock_location_domain(self):
        for rec in self:
            if(rec.x_studio_obra.warehouse_id):
                #Definimos el dominio
                ubicaciones_domain = ["|", ('warehouse_id.id', "=", rec.x_studio_obra.warehouse_id.id), ('location_id.warehouse_id.id', "=", rec.x_studio_obra.warehouse_id.id)]
                return {'domain': {'x_studio_subcontrato': ubicaciones_domain}}

    def _overwrite_obra_domain(self): 
        return ["&",("code","=","incoming"),"|",("warehouse_id","!=",False),("warehouse_id.company_id","=", self.env.company.id)]

    x_studio_obra = fields.Many2one('stock.picking.type', string='Obra', domain=_overwrite_obra_domain)
    x_studio_subcontrato = fields.Many2one('stock.location', string='Concepto (Contrato/Subcontrato)', domain=[('id', '=', '-1')])

    def action_custom_rfq(self):
        for requisition in self:
            purchase_order_count = requisition.env['purchase.order'].search_count([('state', '!=', False)])
            request_for_quotation = requisition.env['purchase.order'].create({
                'company_id': requisition.env.company.id,
                'currency_id': requisition.env.company.currency_id.id,
                'date_order': requisition.date_end,
                # 'name': 'P' + '{:0>5}'.format(purchase_order_count),
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
                'res_id': request_for_quotation_id
            }

            return res