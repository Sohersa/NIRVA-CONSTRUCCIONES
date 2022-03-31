# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    
    _inherit='res.partner'

    es_sucursal = fields.Boolean()
    hide_parent_field = fields.Boolean()

    # Establecemos la acción a ejecutar al cambiar el valor de "is_company"
    @api.onchange('is_company')
    def _onchange_is_company(self):
        for rec in self:
            # Si el contacto en creación/edición es una empresa...
            if (rec.is_company):
                # y es una sucursal...
                if (rec.es_sucursal):
                    # Mostramos el campo de empresa relacionada
                    # rec.hide_parent_id_field = False
                    # retornamos un dominio que sólo incluya a las empresas
                    return {'domain': {'parent_id': ['&', ('is_company', '=', True), ('es_sucursal', '=', False)]}}
                # y no es una sucursal
                else:
                    # Ocultamos el campo de empresa relacionada
                    # rec.hide_parent_id_field = True
                    # retornamos un dominio vacío
                    return {'domain': {'parent_id': [('id', '=', '-1')]}}
                """
                Nota: por consistencia, es importante que el campo de 'parent_id'
                se oculte si el contacto en creación/edición es una empresa; es decir, cuando 
                (is_company & !es_sucursal)
                """
            # Si el contacto en creación/edición no es una empresa...
            else:
                # retornamos un dominio que sólo incluya a las sucursales
                return {'domain': {'parent_id': ['&', ('is_company', '=', True), ('es_sucursal', '=', True)]}}
    
    # Establecemos la acción a ejecutar al cambiar el valor de 'es_sucursal'
    @api.onchange('es_sucursal')
    def _onchange_es_sucursal(self):
        for rec in self:
            # Si el contacto en creación/edición es una empresa...
            if (rec.is_company):
                # y es una sucursal...
                if (rec.es_sucursal):
                    # Mostramos el campo de empresa relacionada
                    # rec.hide_parent_id_field = False
                    # retornamos un dominio que sólo incluya a las empresas
                    return {'domain': {'parent_id': ['&', ('is_company', '=', True), ('es_sucursal', '=', False)]}}
                # y no es una sucursal
                else:
                    # Ocultamos el campo de empresa relacionada
                    # rec.hide_parent_id_field = True
                    # retornamos un dominio vacío
                    return {'domain': {'parent_id': [('id', '=', '-1')]}}
                """
                Nota: por consistencia, es importante que el campo de 'parent_id'
                se oculte si el contacto en creación/edición es una empresa; es decir, cuando 
                (is_company & !es_sucursal)
                """
            # Si el contacto en creación/edición no es una empresa...
            else:
                # retornamos un dominio que sólo incluya a las sucursales
                return {'domain': {'parent_id': ['&', ('is_company', '=', True), ('es_sucursal', '=', True)]}}

class PurchaseOrder(models.Model):

    _inherit='purchase.order'

    # Estableciendo el campo de empresa
    enterprise_domain = ['&', ('is_company', '=', True), ('es_sucursal', '=', False)]
    empresa_id = fields.Many2one('res.partner', string='Empresa', domain=enterprise_domain)

    # Estableciendo el campo de la sucursal
    sucursal_domain = [('id', '=', '-1')]
    sucursal_id = fields.Many2one('res.partner', string='Sucursal', domain=sucursal_domain)

    # Establecemos el dominio de las sucursales
    @api.onchange('empresa_id')
    def _onchange_empresa(self):
        for rec in self:
            return {'domain': {'sucursal_id': [('parent_id', '=', rec.empresa_id.id)]}}

    # Establecemos el dominio de los contactos
    @api.onchange('sucursal_id')
    def _onchange_sucursal(self):
        for rec in self:
            return {'domain': {'partner_id': [('parent_id', '=', rec.sucursal_id.id)]}}

    # def _get_child_partners(self):
    #     domain =[('id', '=', -1)]
    #     partners_list=[]
    #     partners = self.env['res.partner'].search([('parent_id','=',self.empresa_id)])
    #     for each in partners:
    #         partners_list.append(each.id)
    #     if partners_list:
    #         domain =[('id', 'in', partners_list)]
    #         return domain
    #     return domain
