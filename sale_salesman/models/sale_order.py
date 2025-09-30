from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    salesman_id = fields.Many2one('res.partner', string='Vendedor*')
    
    def data_report(self):
        res = super(SaleOrder, self).data_report()
        res.update({
            "salesman_name": self.salesman_id.name or "" if self.salesman_id else "",
            "salesman_email": self.salesman_id.email if self.salesman_id else "",
            "salesman_mobile": self.salesman_id.mobile if self.salesman_id else "",
        })
        return res
    
    
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'salesman_id': self.salesman_id.id
        })
        return invoice_vals