# -*- coding: utf-8 -*-
from odoo import api, fields, models


class RegistroNota(models.Model):
    _name = 'registro.nota'
    _description = 'Registro de Nota'
    _rec_name = 'display_name'

    student_code = fields.Char(string='Código de Alumno', required=True, index=True)
    course_name = fields.Char(string='Curso', required=True)
    career_name = fields.Char(string='Carrera', required=True)
    grade = fields.Float(string='Nota', required=True, digits=(3, 2))
    observation = fields.Text(string='Observaciones')
    display_name = fields.Char(compute='_compute_display_name', store=True)

    _sql_constraints = [
        (
            'registro_nota_unique',
            'unique(student_code, course_name, career_name)',
            'Ya existe una nota registrada para este alumno en el curso y carrera seleccionados.',
        )
    ]

    @api.depends('student_code', 'course_name', 'career_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.student_code} - {record.course_name} ({record.career_name})"
