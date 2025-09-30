from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    salesman_id = fields.Many2one('res.partner', string='Vendedor')
    
    
    def data_report(self):
        res = super(AccountMove, self).data_report()
        res.update({
            "salesman_name": self.salesman_id.name or "" if self.salesman_id else "",
            "salesman_email": self.salesman_id.email if self.salesman_id else "",
            "salesman_mobile": self.salesman_id.mobile if self.salesman_id else "",
        })
        return res