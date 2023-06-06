# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    # Extendemos del modelo de factura
    _inherit = 'account.move'

    # Estableciendo un dominio de contactos que sean empresas y que no estén asociados a otro contacto
    enterprise_domain = ['&', ('is_company', '=', True),
                         ('parent_id', '=', False)]
    # Declaramos un campo para filtrar a los proveedores en función a su empresa o agrupación
    empresa_id = fields.Many2one(
        'res.partner', string='Empresa', domain=enterprise_domain)
    partner_id = fields.Many2one('res.partner', string='Proveedor')

    # Establecemos el dominio de los proveedores al cambiar el campo de empresa
    @api.onchange('empresa_id')
    def _onchange_empresa(self):
        for rec in self:
            # Si se hay una empresa establecida...
            if (rec.empresa_id):
                # devolvemos los partners que estén asociados a la misma
                return {'domain': {'partner_id': [('parent_id', '=', rec.empresa_id.id)]}}
            # Caso contrario...
            else:
                # Devolvemos todos los partners individuales que no estén asociados a ninguna compañía
                return {'domain': {'partner_id': ['&', ('is_company', '=', False), ('parent_id', '=', False)]}}

    # Establecemos el dominio de las cuentas bancarias al cambiar el partner_id
    @api.onchange('partner_id')
    def _onchange_partner(self):
        for rec in self:
            # Si hay un partner establecido
            if (rec.partner_id):
                # Revisamos si el partner es un contacto o una sucursal de algún otro partner
                if (rec.partner_id.parent_id):
                    # Buscamos todas las cuentas que pertenezcan al parent del contacto
                    # donde, además, el contacto de sucursal sea igual al contacto establecido.
                    partner_banks_ids = self.env['res.partner.bank'].search([
                        ('partner_id', '=', rec.partner_id.parent_id.id),
                        ('oupp_contacto_de_sucursal', '=', rec.partner_id.id)
                    ])
                # Si el partner no es un contacto o una sucursal
                else:
                    # Retornamos todas las cuentas que pertenezcan al partner
                    partner_banks_ids = self.env['res.partner.bank'].search([
                        ('partner_id', '=', rec.partner_id.id)
                    ])

            # Revisamos si había cuentas bancarias con las condiciones dadas
            if partner_banks_ids and len(partner_banks_ids) >= 1:
                # Establecemos la primer cuenta de la tupla en el campo correspondiente
                rec['partner_bank_id'] = partner_banks_ids[0]
                # Retornamos el dominio para el campo con las cuentas encontradas
                return {'domain': {'partner_bank_id': partner_banks_ids}}
            else:
                # Retornamos un dominio sin filtros
                return {'domain': {'partner_bank_id': []}}

    # Referencia de la factura
    ref = fields.Char(string="Referenia UUID")

    # Archivo de la factura timbrada
    factura_sat = fields.Binary(string="Factura SAT")

    # Creamos el campo de tipo de pago
    oupp_tipo_de_pago = fields.Selection(
        related="oupp_po.tipo_de_pago", string="Tipo de pago")

    # Recuperamos el regimen fiscal directamente desde el partner
    oupp_regimen_fiscal = fields.Selection(
        related="partner_id.regimen_fiscal", string="Regimen Fiscal")

    # Abrimos la vista con el pago o la lista de pagos relacionadas a la factura
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

    # Obtenemos el número de pagos donde la ref corresponda al nombre de esta factura
    def get_payments_count(self):
        payments_count = self.env['account.payment'].search_count(
            [('ref', '=', self.name)])
        self.oupp_payments_count = payments_count

    # Campo computado con la cantidad de pagos asociados a la factura
    oupp_payments_count = fields.Integer(
        string='Pagos', compute="get_payments_count")

    # CAMPOS RELACIONALES
    # Orden de compra
    oupp_po = fields.Many2one("purchase.order", string="Orden de compra")
    # Orden de compra - Referencia interna
    oupp_po_ref = fields.Char(
        string="Orden de compra (Referencia interna)", related="oupp_po.x_studio_referencia")
    # Obra
    oupp_obra = fields.Many2one(
        "stock.picking.type", string="Obra", related="oupp_po.picking_type_id", store=True)
    # Concepto
    oupp_concepto = fields.Many2one(
        "stock.location", string="Concepto (Contrato/Subcontrato)", related="oupp_po.x_subcontrato", store=True)
    # Autorizado por
    oupp_autoriza = fields.Many2one(
        "hr.employee", string="Autorizado por", related="oupp_po.autoriza")

    # Manejamos el cambio del campo
    @api.onchange('oupp_po')
    # Filtramos el dominio del campo hr.expense.nirva_contrato [Concepto]
    def _set_related_fields(self):
        for move in self:
            # Verificamos que se haya establecido una orden de compra
            if (move.oupp_po):
                move["purchase_id"] = move.oupp_po
                move["partner_id"] = move.oupp_po.partner_id
                move["empresa_id"] = move.oupp_po.empresa_id
