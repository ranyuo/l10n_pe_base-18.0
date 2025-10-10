from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduAcademicPeriod(models.Model):
    _name = "edu.academic.period"
    _description = "Periodos Academicos"

    name = fields.Char(string="Nombre", required=True)