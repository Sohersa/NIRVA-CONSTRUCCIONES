# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerBankExtension(models.Model):
    _inherit = 'res.partner.bank'

    referencia_bancaria = fields.Char(string="Referencia bancaria")

    # Declaramos un campo para asociar la cuenta bancaria a algún contacto del partner
    oupp_contacto_de_sucursal = fields.Many2one('res.partner', string='Contacto de sucursal')

    # Establecemos el dominio de los contactos al cambiar de partner
    @api.onchange('partner_id')
    def _onchange_partner(self):
        for rec in self:
            # Si se hay un partner establecido...
            if(rec.partner_id):
                # Devolvemos los contactos que estén asociados al mismo
                return {'domain': {'oupp_contacto_de_sucursal': [('parent_id', '=', rec.partner_id.id)]}}
            # Caso contrario...
            else:
                # Devolvemos un rango vacío.
                return {'domain': {'oupp_contacto_de_sucursal': []}}
            
