from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduClassSchedule(models.Model):
    _name = "edu.class.schedule"
    _description = "Horarios de clase"

    name = fields.Char(string="Nombre", default="New")
    course_id = fields.Many2one("edu.course", string="Curso")
    career_id = fields.Many2one("edu.career", string="Carrera")
    academic_period_id = fields.Many2one("edu.academic.period", string="Semestre")
    partner_id = fields.Many2one("res.partner", string="Docente")
    class_type = fields.Selection([
        ('teoria', 'Teoría'),
        ('practica', 'Práctica'),
        ('laboratorio', 'Laboratorio'),
        ('virtual', 'Virtual')
    ], string='Tipo')
    classroom_id = fields.Many2one("edu.classroom", string="Aula")
    link = fields.Char(string="Enlace")
    start_class = fields.Datetime(string="Inicio de clase")
    end_class = fields.Datetime(string="Fin de clase")
    duration = fields.Integer(string="Duración(minutos)", compute="_compute_duration", store=True, readonly=False)
    break_time = fields.Integer(string="Break(minutos)", default=0.0)


    @api.depends('start_class', 'end_class')
    def _compute_duration(self):
        for record in self:
            if record.start_class and record.end_class:
                delta = record.end_class - record.start_class
                record.duration = int(delta.total_seconds() / 60)
            else:
                record.duration = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                if vals.get('course_id') and vals.get('career_id'):
                    course = self.env['edu.course'].browse(vals['course_id'])
                    career = self.env['edu.career'].browse(vals['career_id'])
                    vals['name'] = f"{course.name} - {career.name}"
        res = super(EduClassSchedule, self).create(vals_list)
        return res