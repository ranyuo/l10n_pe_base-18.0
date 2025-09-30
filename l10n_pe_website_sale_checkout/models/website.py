from odoo import fields, models, api

class Website(models.Model):
    _inherit = "website"
    
    show_address_in_checkout = fields.Boolean(
        string="Requerir dirección en el checkout",
        default=True
    )
    
    require_identity_document_for_invoice = fields.Boolean(
        string="Requerir documento de identidad de Comprador",
        default=True
    )

    