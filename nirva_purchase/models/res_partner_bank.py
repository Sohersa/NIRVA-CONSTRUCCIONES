# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartnerBankExtension(models.Model):
    _inherit = 'res.partner.bank'

    referencia_bancaria = fields.Char(string="Referencia bancaria")