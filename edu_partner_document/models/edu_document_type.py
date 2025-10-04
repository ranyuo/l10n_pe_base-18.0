from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduDocumentType(models.Model):
    _name = "edu.document.type"
    _description = "Tipo de documento"

    name = fields.Char(string="Nombre", required=True)
    code = fields.Char(string="Código")
    description = fields.Text(string="Descripción")