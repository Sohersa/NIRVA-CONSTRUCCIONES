# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):

    _inherit='purchase.order'

    enterprise_domain = [('company_type', '=', 'company')]
    empresa_id = fields.Many2one('res.partner', string='Empresa', domain=enterprise_domain)

    def _get_child_partners(self):
        domain =[('id', '=', -1)]
        partners_list=[]
        partners = self.env['res.partner'].search([('parent_id','=',self.empresa_id)])
        for each in partners:
            partners_list.append(each.id)
        if partners_list:
            domain =[('id', 'in', partners_list)]
            return domain
        return domain

    @api.onchange('empresa_id')
    def _onchange_empresa(self):
        for rec in self:
            return {'domain': {'partner_id': [('parent_id', '=', rec.partner_id.id)]}}
    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100