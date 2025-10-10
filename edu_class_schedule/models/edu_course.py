from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduCourse(models.Model):
    _name = "edu.course"
    _description = "Cursos"

    name = fields.Char(string="Nombre", required=True)