from odoo import models,fields,api


class SaleReport(models.Model):
    _inherit = 'sale.report'
    
    salesman_id = fields.Many2one('res.partner', string='Vendedor*', readonly=True)
    
    def _select_sale(self):
        select_str = super()._select_sale()
        select_str += ", s.salesman_id as salesman_id"
        return select_str
    
    def _from_sale(self):
        from_str = super()._from_sale()
        from_str += " LEFT JOIN res_partner sm ON sm.id = s.salesman_id"
        return from_str
    
    