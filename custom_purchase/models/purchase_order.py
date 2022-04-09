# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):

    _inherit='purchase.order'

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