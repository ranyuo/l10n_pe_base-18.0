from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduEducationalInstitution(models.Model):
    _name = "edu.educational.institution"
    _description = "Institución educativa"

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Código")
    description = fields.Text(string="Descripción")