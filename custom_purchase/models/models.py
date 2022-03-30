# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    # _name = 'my_module.custom_purchase'
    _inherit='purchase.order'

    enterprise_domain = [('company_type', '=', 'company')]
    empresa_id = fields.Many2one('res.partner', string='Empresa', domain=enterprise_domain)
    # name = fields.Char()
    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    # description = fields.Text()

    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100