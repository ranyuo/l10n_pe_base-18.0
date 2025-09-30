from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_salesman = fields.Boolean(string="Es Vendedor", default=False)
    
    signature_salesman = fields.Html(string="Firma Vendedor")