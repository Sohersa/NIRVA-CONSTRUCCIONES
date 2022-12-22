# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    # Extendemos del modelo de factura
    _inherit = 'account.move'

    # Referencia de la factura
    ref = fields.Char(string="Referenia UUID")

    # Archivo de la factura timbrada
    factura_sat = fields.Binary(string="Factura SAT")

    # Creamos el campo de tipo de pago
    oupp_tipo_de_pago = fields.Selection(related="oupp_po.tipo_de_pago", string="Tipo de pago")

    # Recuperamos el regimen fiscal directamente desde el partner
    oupp_regimen_fiscal = fields.Selection(related="partner_id.regimen_fiscal", string="Regimen Fiscal")

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
        payments_count = self.env['account.payment'].search_count([('ref', '=', self.name)])
        self.payments_count = payments_count

    # Campo computado con la cantidad de pagos asociados a la factura
    oupp_payments_count = fields.Integer(string='Pagos', compute="get_payments_count")

    # CAMPOS RELACIONALES
    # Orden de compra 
    oupp_po = fields.Many2one("purchase.order", string="Orden de compra")
    # Orden de compra - Referencia interna
    oupp_po_ref = fields.Char(string="Orden de compra (Referencia interna)", related="oupp_po.x_studio_referencia")
    # Obra
    oupp_obra = fields.Many2one("stock.picking.type", string="Obra", related="oupp_po.picking_type_id")
    # Concepto
    oupp_concepto = fields.Many2one("stock.location", string="Concepto (Contrato/Subcontrato)", related="oupp_po.x_subcontrato")
    # Autorizado por
    oupp_autoriza = fields.Many2one("hr.employee", string="Autorizado por", related="oupp_po.autoriza")

    # Manejamos el cambio del campo 
    @api.onchange('oupp_po')
    # Filtramos el dominio del campo hr.expense.nirva_contrato [Concepto]
    def _set_related_fields(self):
        for move in self:
            # Verificamos ha establecido una orden de compra
            if(move.oupp_po):
                move["purchase_id"] = move.oupp_po
 