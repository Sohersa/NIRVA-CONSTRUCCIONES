# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    ref = fields.Char(string="Referenia UUID")

    regimen_fiscal = fields.Selection([('Asalariados','Servicios profesionales (honorarios)','Arrendamiento de inmuebles','Actividad empresarial','Incorporación fiscal','General','Personas morales con fines no lucrativos')], string="Regimen Fiscal", related="partner_id.regimen_fiscal")