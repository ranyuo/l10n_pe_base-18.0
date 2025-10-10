from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduClassroom(models.Model):
    _name = "edu.classroom"
    _description = "Aulas"

    name = fields.Char(string="Nombre", required=True)