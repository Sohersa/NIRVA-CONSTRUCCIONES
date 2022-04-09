# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartnerExtension(models.Model):
    _inherit = 'res.partner'

    @api.constrains('vat', 'country_id')
    def check_vat_extended(self):
        return True

    ResPartner.check_vat = check_vat_extended