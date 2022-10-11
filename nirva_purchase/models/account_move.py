# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    ref = fields.Char(string="Referenia UUID")
    factura_sat = fields.Binary(string="Factura SAT")

    def _regimenes_fiscales(self):
        return [
            ('Asalariados', 'Asalariados'), 
            ('Servicios profesionales (honorarios)','Servicios profesionales (honorarios)'),
            ('Arrendamiento de inmuebles', 'Arrendamiento de inmuebles'),
            ('Actividad empresarial', 'Actividad empresarial'),
            ('Incorporación fiscal', 'Incorporación fiscal'),
            ('General', 'General'),
            ('Personas morales con fines no lucrativos', 'Personas morales con fines no lucrativos')
        ]

    def open_account_move_payments(self):
        return {
            'name': 'Pagos',
            'domain': [('ref', '=', self.name)],
            'view_type': 'form',
            'res_model': 'account.payment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def get_payments_count(self):
        payments_count = self.env['account.payment'].search_count([('ref', '=', self.name)])
        self.payments_count = payments_count

    regimen_fiscal = fields.Selection(selection='_regimenes_fiscales', string="Regimen Fiscal", related="partner_id.regimen_fiscal")
    payments_count = fields.Integer(string='Pagos', compute="get_payments_count")