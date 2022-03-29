# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    
    _inherit='purchase.order'

    enterprise_domain = [('company_type', '=', 'company')]

    empresa_id = fields.Many2one('res.partner', 'Empresa', domain=enterprise_domain)