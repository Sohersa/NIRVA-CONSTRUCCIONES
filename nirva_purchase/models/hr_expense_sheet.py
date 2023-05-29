# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrExpenseSheet(models.Model):
    #Extendemos el modelo de gastos
    _inherit='hr.expense.sheet'

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
    nirva_obra = fields.Many2one('stock.picking.type', string='Obra', domain=_overwrite_obra_domain)
    # Generamos un atributo que nos permita ligar el gasto a las ubicaciones de un almacén (contrato o subcontrato de una obra)
    nirva_contrato = fields.Many2one('stock.location', string='Concepto (Contrato/Subcontrato)', domain=[('id', '=', '-1')])

    # Manejamos el cambio del contrato 
    @api.onchange('nirva_obra', 'nirva_contrato')
    # Verificamos la consistencia en las obras (warehouses) y los contratos (locations)
    def _check_consistent_location_and_wharehouse(self):
        for rec in self:
            # Verificamos que exista un alamacén y una ubicación establecida
            if (rec.nirva_obra.warehouse_id or rec.nirva_contrato.id):
                # Iteramos sobre las líneas de gastos incluídas en el reporte
                for expense in rec.expense_line_ids:
                    # Revisamos si tanto el gasto como el reporte tienen un almacén
                    if (expense.nirva_obra.warehouse_id and rec.nirva_obra.warehouse_id):
                        # Revisamos si hay alguna variación en el almacén 
                        if (expense.nirva_obra.warehouse_id != rec.nirva_obra.warehouse_id):
                            # Mostramos un error de validación
                            raise ValidationError(_("Verifique que todos los gastos pertenezcan a la misma obra."))
                    # Revisamos si tanto el gasto como el reporte tienen una ubicación
                    if (expense.nirva_contrato.id and rec.nirva_contrato.id):
                        # Revisamos si hay alguna variación en la ubicación 
                        if (expense.nirva_contrato.id != rec.nirva_contrato.id):
                            # Mostramos un error de validación
                            raise ValidationError(_("Verifique que todos los gastos pertenezcan al mismo contrato."))
