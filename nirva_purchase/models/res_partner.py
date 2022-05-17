# -*- coding: utf-8 -*-

from odoo.addons.base_vat.models.res_partner import ResPartner
from odoo import models, fields, api

class ResPartnerExtension(models.Model):
    _inherit = 'res.partner'

    regimen_fiscal = fields.Selection([('Asalariados','Servicios profesionales (honorarios)','Arrendamiento de inmuebles','Actividad empresarial','Incorporación fiscal','General','Personas morales con fines no lucrativos')], string="Regimen Fiscal")

    # Configuramos el regimen fiscal al cambiar la naturaleza del contacto
    @api.onchange('is_company', 'parent_id')
    def _set_regimen_fiscal(self):
        for rec in self:
            # Si el contacto es un contacto indivudual y está asociado a una empresa,
            # entonces, hereda sus datos bancarios de la empresa relacionada...
            if (not rec.is_company and rec.parent_id):
                # Por tanto, el regimen fiscal debe ser el mismo que la empresa relacionada
                rec['regimen_fiscal'] = rec.parent_id.regimen_fiscal


    @api.constrains('vat', 'country_id')
    def check_vat_extended(self):
        return True

    ResPartner.check_vat = check_vat_extended