# -*- coding: utf-8 -*-

from odoo.addons.base_vat.models.res_partner import ResPartner
from odoo import models, api

class ResPartnerExtension(models.Model):
    _inherit = 'res.partner'

    @api.constrains('vat', 'country_id')
    def check_vat_extended(self):
        return True

    ResPartner.check_vat = check_vat_extended