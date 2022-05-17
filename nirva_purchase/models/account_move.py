# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    ref = fields.Char(string="Referenia UUID")

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
    # regimen_fiscal = fields.Selection(selection='_regimenes_fiscales', string="Regimen Fiscal", related="partner_id.regimen_fiscal")
    regimen_fiscal = fields.Selection(selection='_regimenes_fiscales', string="Regimen Fiscal")