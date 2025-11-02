# -*- coding: utf-8 -*-
from odoo import api, fields, models


class RegistroNota(models.Model):
    _name = 'registro.nota'
    _description = 'Registro de Nota'
    _rec_name = 'display_name'

    student_id = fields.Many2one(
        'res.partner',
        string='Alumno',
        required=True,
        ondelete='restrict',
        domain="[('is_company', '=', False)]",
        index=True,
    )
    student_code = fields.Char(
        string='Código de Alumno',
        compute='_compute_student_code',
        store=True,
        readonly=True,
        index=True,
        help='Se obtiene del campo Referencia del contacto del alumno.',
    )
    course_id = fields.Many2one('registro.curso', string='Curso', required=True, ondelete='restrict')
    career_id = fields.Many2one(
        'registro.carrera',
        string='Carrera',
        related='course_id.career_id',
        store=True,
        readonly=True,
    )
    grade = fields.Float(string='Nota', required=True, digits=(3, 2))
    observation = fields.Text(string='Observaciones')
    display_name = fields.Char(compute='_compute_display_name', store=True)

    _sql_constraints = [
        (
            'registro_nota_unique',
            'unique(student_id, course_id)',
            'Ya existe una nota registrada para este alumno en el curso seleccionado.',
        )
    ]

    @api.depends('student_id.ref', 'student_id.vat', 'student_id.name')
    def _compute_student_code(self):
        for record in self:
            record.student_code = record.student_id.ref or record.student_id.vat or ''

    @api.depends('student_id', 'course_id', 'career_id')
    def _compute_display_name(self):
        for record in self:
            student = record.student_id.name or record.student_code or 'Alumno'
            course = record.course_id.name or 'Curso'
            career = record.career_id.name or 'Carrera'
            record.display_name = f"{student} - {course} ({career})"
