from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduCareer(models.Model):
    _name = "edu.career"
    _description = "Carreras"

    name = fields.Char(string="Nombre", required=True)