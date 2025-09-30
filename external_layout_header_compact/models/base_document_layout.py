from odoo import models,fields,api

class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"

    street = fields.Char('Dirección', related='company_id.street') 
    
    
    show_default_code_invoice = fields.Boolean(
        string='Mostrar código interno en facturas',
        default=False,
        readonly=False,
        related="company_id.show_default_code_invoice",
        help='Muestra el código interno (referencia interna) del producto en una columna separada en las facturas de venta'
    )

    show_default_code_quotation = fields.Boolean(
        string='Mostrar código interno en cotizaciones', 
        default=False,
        readonly=False,
        related="company_id.show_default_code_quotation",
        help='Muestra el código interno (referencia interna) del producto en una columna separada en las cotizaciones'
    )
    
    show_subtotal_pen = fields.Boolean(
        string='Mostrar subtotales en PEN',
        default=False,
        readonly=False,
        related="company_id.show_subtotal_pen",
        help='Muestra los subtotales en soles (PEN) al tipo de cambio del día cuando se cotiza en otra moneda'
    )
    
    @api.onchange('company_id')
    def _onchange_company_id(self):
        super()._onchange_company_id()
        for wizard in self:
            wizard.show_default_code_invoice = wizard.company_id.show_default_code_invoice
            wizard.show_default_code_quotation = wizard.company_id.show_default_code_quotation
            wizard.show_subtotal_pen = wizard.company_id.show_subtotal_pen