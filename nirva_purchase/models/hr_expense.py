# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrExpense(models.Model):
    #Extendemos el modelo de gastos
    _inherit='hr.expense'

    # Manejamos el cambio del campo 
    @api.onchange('nirva_obra')
    # Filtramos el dominio del campo hr.expense.nirva_contrato [Concepto]
    def _set_stock_location_domain(self):
        for rec in self:
            # Verificamos que exista un almacén establecido
            if(rec.nirva_obra.warehouse_id):
                #Definimos el dominio a aquellos cuya ubicación (contrato) pertenezca al almacén del tipo de movimiento
                ubicaciones_domain = ["|", ('warehouse_id.id', "=", rec.nirva_obra.warehouse_id.id), ('location_id.warehouse_id.id', "=", rec.nirva_obra.warehouse_id.id)]
                return {'domain': {'nirva_contrato': ubicaciones_domain}}
    # Establecemos el dominio del tipo de movimiento a las recepciones de los almacenes de la compañía
    def _overwrite_obra_domain(self): 
        return ["&",("code","=","incoming"),"|",("warehouse_id","!=",False),("warehouse_id.company_id","=", self.env.company.id)]

    # Generamos un atributo que nos permita ligar el gasto a las recepciones de un almacén (representativo de una obra)
    nirva_obra = fields.Many2one('stock.picking.type', string='Obra', domain=_overwrite_obra_domain, tracking=True)
    # Generamos un atributo que nos permita ligar el gasto a las ubicaciones de un almacén (contrato o subcontrato de una obra)
    nirva_contrato = fields.Many2one('stock.location', string='Concepto (Contrato/Subcontrato)', domain=[('id', '=', '-1')], tracking=True)