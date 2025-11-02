# -*- coding: utf-8 -*-
from odoo import fields, models


class RegistroCarrera(models.Model):
    _name = 'registro.carrera'
    _description = 'Carrera Académica'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True, translate=True)
    code = fields.Char(string='Código', required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('registro_carrera_code_unique', 'unique(code)', 'El código de la carrera debe ser único.'),
    ]


class RegistroCurso(models.Model):
    _name = 'registro.curso'
    _description = 'Curso Académico'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True, translate=True)
    code = fields.Char(string='Código', required=True)
    career_id = fields.Many2one('registro.carrera', string='Carrera', required=True, ondelete='restrict')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('registro_curso_code_unique', 'unique(code)', 'El código del curso debe ser único.'),
    ]
