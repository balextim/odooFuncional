from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date

class trabajadores(models.Model):
    _name='trabajadores.trabajadores'
    _description='modelo para los trabajadores'

    name = fields.Char('DNI', required=True)
    nombre =fields.Char(String='nombre',required=True)
    apellido =fields.Char(String='apellido',required=True)
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento', required=True)
    edad =fields.Integer(String="Edad", compute="_get_edad")
    telefono = fields.Char(String='telefono',required=True)
    puesto = fields.Many2one('trabajadores.puesto', String='puesto')
    horario = fields.One2many('trabajadores.horario', 'idTrabajador', String='horario')

    @api.depends('fecha_nacimiento')
    def _get_edad(self):
        for trabajador in self:
            hoy = date.today()
            trabajador.edad = relativedelta(hoy, trabajador.fecha_nacimiento).years

class puesto(models.Model):
    _name='trabajadores.puesto'
    _description='modelo puesto de los trabajadores'

    name = fields.Char('id', required=True)
    puesto = fields.Char(String='puesto', required=True)
    trabajador = fields.One2many('trabajadores.trabajadores', 'puesto', String='empleado')

class horario(models.Model):
    _name='trabajadores.horario'
    _description='modelo para los horarios de los trabajadores'

    name = fields.Char('id', required=True)
    idTrabajador = fields.Many2one('trabajadores.trabajadores', String='idTrabajador', required=True)
    fecha=fields.Date(String='fecha', required=True)
    hora_entrada = fields.Float(String='hora_entrada')
    hora_salida = fields.Float(String='hora_salida')
    horas_trabajo = fields.Float(String='horas_trabajo', compute="_get_horas_trabajo")
    total_pagar = fields.Float(String='total_pagar', compute="_get_total_pagar")

    #función para calcular horas de trabajo
    @api.depends('hora_entrada')
    def _get_horas_trabajo(self):
        for horas in self:
            if horas.hora_salida > horas.hora_entrada:
                horas.horas_trabajo = horas.hora_salida - horas.hora_entrada
            elif horas.hora_salida < horas.hora_entrada:
                horas.horas_trabajo = horas.hora_salida-horas.hora_entrada+24

    @api.depends('horas_trabajo')
    def _get_total_pagar(self):
        for horas in self:
            horas.total_pagar = horas.horas_trabajo * 10