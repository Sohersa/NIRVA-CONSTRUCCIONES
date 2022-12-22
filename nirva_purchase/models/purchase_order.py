# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):

    _inherit='purchase.order'

    # Retomamos el campo de quien autoriza
    autoriza = fields.Many2one("hr.employee", string="Autorizado por", related="requisition_id.autoriza")
    
    partner_id = fields.Many2one('res.partner', string='Proveedor', required=False)

    # Estableciendo el campo de empresa
    enterprise_domain = ['&', ('is_company', '=', True), ('parent_id', '=', False)]
    empresa_id = fields.Many2one('res.partner', string='Empresa', domain=enterprise_domain)

    # Establecemos el dominio de los proveedores al cambiar el campo de empresa
    @api.onchange('empresa_id')
    def _onchange_empresa(self):
        for rec in self:
            # Si se hay una empresa establecida...
            if(rec.empresa_id):
                # devolvemos los partners que estén asociados a la misma
                return {'domain': {'partner_id': [('parent_id', '=', rec.empresa_id.id)]}}
            # Caso contrario...
            else:
                # Devolvemos todos los partners individuales que no estén asociados a ninguna compañía
                return {'domain': {'partner_id': ['&', ('is_company', '=', False), ('parent_id', '=', False)]}}

    # Limitamos el dominio del campo purchase.picking_type_id [Obra]
    @api.onchange('requisition_id')
    def _set_picking_type_domain(self):
        for rec in self:
            # Definimos el dominio
            obra_domain = ["&",("code","=","incoming"),"|",("warehouse_id","!=",False),("warehouse_id.company_id","=", rec.env.company.id)]
            return {'domain': {'picking_type_id': obra_domain}}

    # Filtramos el dominio del campo purchase_order.x_subcontrato [Concepto]
    @api.onchange('picking_type_id')
    def _set_stock_location_domain(self):
        for rec in self:
            if(rec.picking_type_id.warehouse_id):
                #Definimos el dominio de las ubicaciones
                ubicaciones_domain = ["|", ('warehouse_id.id', "=", rec.picking_type_id.warehouse_id.id), ('location_id.warehouse_id.id', "=", rec.picking_type_id.warehouse_id.id)]
                return {'domain': {'x_subcontrato': ubicaciones_domain}}