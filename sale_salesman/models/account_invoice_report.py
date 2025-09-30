from odoo import models, fields, api
from odoo.tools import SQL

class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'
    
    salesman_id = fields.Many2one('res.partner', string='Vendedor*', readonly=True)
    
    def _select(self) -> SQL:
        return SQL("%s, move.salesman_id as salesman_id", super()._select())
    
    def _from(self):
        return SQL("%s LEFT JOIN res_partner sm ON sm.id = move.salesman_id", super()._from())