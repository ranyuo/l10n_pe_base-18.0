import logging
from odoo import api, models, _, fields
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]

class LibroReclamaciones(models.Model):
    _name = "libro.reclamaciones"
    _description = "Libro de reclamaciones"
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    state = fields.Selection(string="Estado", selection=[('new', 'Nuevo'),
                                                         ('in_process','En proceso'),
                                                         ('cancel', 'Cancelado'),
                                                         ('resolved', 'Resuelto')],
                             default="new",
                             group_expand='_read_group_stage_ids',
                             tracking=True)

    @api.model
    def _read_group_stage_ids(self, states, domain):
        return ['new',
                'in_process',
                'resolved',
                'cancel', ]

    # IDENTIFICACIÓN DEL CONSUMIDOR RECLAMANTE
    consumer_type = fields.Selection(selection=[('individual', 'Persona Natural'), (
                                                'company', 'Empresa')], 
                                    string="Tipo de consumidor", 
                                    default="individual")
    consumer_company_name = fields.Char(string="Razón Social")
    consumer_company_document = fields.Char(string="N° R.U.C.")

    consumer_name = fields.Char(string="Nombres")
    consumer_lastname = fields.Char(string="Apellidos")
    consumer_email = fields.Char(string="E-mail")
    consumer_document_type = fields.Selection(string="Tipo de documento de Identidad", selection=[
                                              ('1', 'DNI'), ('4', 'CE'), ('7', 'Pasaporte')], default="1")
    consumer_document = fields.Char(string="Número de documento")
    consumer_phone = fields.Char(string="Teléfono")
    consumer_address = fields.Char(string="Dirección")

    consumer_country_id = fields.Many2one("res.country", default=lambda r: r.env.ref("base.pe", raise_if_not_found=False))
    consumer_state_id = fields.Many2one("res.country.state", string="Departamento")
    consumer_province_id = fields.Many2one("res.city", string="Provincia")
    consumer_district_id = fields.Many2one("l10n_pe.res.city.district", string="Distrito")

    # DATOS DEL PADRE, MADRE O TUTOR
    consumer_younger = fields.Boolean(string="Es menor de edad?", default=False)
    consumer_younger_name = fields.Char(string="Nombres")
    consumer_younger_lastname = fields.Char(string="Apellidos")
    consumer_younger_document = fields.Char(string="DNI/CE")

    # IDENTIFICACIÓN DEL BIEN CONTRATADO
    product_type = fields.Selection(string="Tipo de producto", selection=[('product', 'Producto'), ('service', 'Servicio')], default="product")
    product_code = fields.Char(string="Código de producto")
    order_name = fields.Char(string="Número de órden de venta")
    date_order = fields.Date(string="Fecha de venta")
    product_name = fields.Char(string="Nombre de producto")

    # DETALLE DE RECLAMO O QUEJA
    claim_type = fields.Selection(string="Tipo de reclamación", selection=[
                                  ('reclamo', 'Reclamo'), ('queja', 'Queja')], default="reclamo")
    claim_amount = fields.Float(string="Monto reclamado")
    claim_detail = fields.Text(string="Detalle de reclamo")
    claim_request = fields.Text(string="Solicitud de reclamo")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id.id)
    name = fields.Char("Número de Reclamo")
    claim_user_id = fields.Many2one("res.users", default=lambda self: self.env.company.default_claim_user_id.id)
    
    priority = fields.Selection(
        AVAILABLE_PRIORITIES, string='Priority', index=True,
        default=AVAILABLE_PRIORITIES[0][0])

    @api.model_create_multi
    def create(self, vals):
        result = super(LibroReclamaciones, self).create(vals)
        sequence = self.env["ir.sequence"].search([("code","=","seq.libro.reclamaciones")])

        if not sequence.exists():
            sequence = self.env["ir.sequence"].create({
                "name": "Secuencia de reclamación LR",
                "implementation": "no_gap",
                "prefix": "LR-",
                "padding": 5,
                "use_date_range": False,
                "number_increment": 1,
                "code": "seq.libro.reclamaciones",
            })

        name = sequence.next_by_id()
        result.update({"name": name})

        return result

    def action_in_process(self):
        if self.state == 'new':
            self.state = 'in_process'
            return
        raise UserError(
            "Para pasar al reclamo en proceso, su estado debe ser Nuevo")

    def action_revert(self):
        if self.state == 'cancel':
            self.state = 'in_process'
            return
        raise UserError(
            "Para pasar al reclamo en proceso, su estado debe ser Cancelado")

    def action_claim_cancel(self):
        if self.state in ['new', 'in_process']:
            self.state = 'cancel'
            return
        raise UserError(
            "Para cancelar el reclamo, su estado debe ser Nuevo o En proceso")

    def action_claim_resolved(self):
        if self.state in ['in_process']:
            self.state = 'resolved'
            return
        raise UserError(
            "Para resolver el reclamo, su estado debe ser En proceso")

    def action_claim_sent(self):
        self.ensure_one()
        template = self.env.ref('l10n_pe_libro_reclamaciones.mail_template_libro_reclamaciones', raise_if_not_found=False)

        ctx = dict(
            default_model='libro.reclamaciones',
            default_res_ids=self.ids,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            force_email=True
        )
        
        return {
            'name': "Enviar Reclamación",
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
        }
