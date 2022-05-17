# -*- coding: utf-8 -*-

from odoo.addons.base_vat.models.res_partner import ResPartner
from odoo import models, fields, api

class ResPartnerExtension(models.Model):
    _inherit = 'res.partner'

    def _regimenes_fiscales():
        return [
            ('Asalariados', 'Asalariados'), 
            ('Servicios profesionales (honorarios)','Servicios profesionales (honorarios)'),
            ('Arrendamiento de inmuebles', 'Arrendamiento de inmuebles'),
            ('Actividad empresarial', 'Actividad empresarial'),
            ('Incorporación fiscal', 'Incorporación fiscal'),
            ('General', 'General'),
            ('Personas morales con fines no lucrativos' 'Personas morales con fines no lucrativos')
        ]
    # regimen_fiscal = fields.Selection(selection='_regimenes_fiscales', string="Regimen Fiscal")

    # Configuramos el regimen fiscal al cambiar la naturaleza del contacto
    # @api.onchange('is_company', 'parent_id')
    # def _set_regimen_fiscal(self):
    #     for rec in self:
    #         # Si el contacto es un contacto indivudual y está asociado a una empresa,
    #         # entonces, hereda sus datos bancarios de la empresa relacionada...
    #         if (not rec.is_company and rec.parent_id and rec.parent_id.regimen_fiscal):
    #             # Por tanto, el regimen fiscal debe ser el mismo que la empresa relacionada
    #             rec['regimen_fiscal'] = rec.parent_id.regimen_fiscal


    @api.constrains('vat', 'country_id')
    def check_vat_extended(self):
        return True

    ResPartner.check_vat = check_vat_extended