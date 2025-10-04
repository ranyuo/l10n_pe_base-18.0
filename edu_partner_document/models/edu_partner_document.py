from odoo import models, api, fields, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class EduPartnerDocument(models.Model):
    _name = "edu.partner.document"
    _description = "Documento de contacto"

    name = fields.Char(string="Nombre", required=True)
    partner_id = fields.Many2one("res.partner", string="Contacto")
    partner_vat = fields.Char(string="DNI")
    partner_code = fields.Char(string="Código")
    partner_phone = fields.Char(string="Teléfono")
    partner_email = fields.Char(string="Correo electrónico")
    document_type = fields.Many2one("edu.document.type", string="Tipo de documento")
    issue_date = fields.Date(string="Fecha de emisión")
    total_hours = fields.Integer(string="Total de horas")
    educational_institution_id = fields.Many2one("edu.educational.institution", string="Institución educativa")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('progress', 'En progreso'),
        ('done', 'Listo')
        ], string="Estado", default='draft')
    start_date = fields.Date(string="Fecha de inicio")
    end_date = fields.Date(string="Fecha de fin")
    file = fields.Binary(string="Archivo")
    filename = fields.Char(string="Nombre de archivo")
    description = fields.Text(string="Descripción")

    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.partner_vat = self.partner_id.vat
        self.partner_phone = self.partner_id.phone
        self.partner_email = self.partner_id.email