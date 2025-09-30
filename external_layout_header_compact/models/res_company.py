from odoo import models, fields, api

DEFAULT_MESSAGE = """Representación impresa de la Facturación electrónica. Consulte el documento en https://consulta-validez. Autorizado mediante resolución SUNAT/2023"""


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_pe_edi_qr_comment_report_invoice_document = fields.Text(string='Mensaje de representación impresa',
                                                                 default=DEFAULT_MESSAGE)
    
    show_default_code_invoice = fields.Boolean(
        string='Mostrar código interno en facturas',
        default=False,
        help='Muestra el código interno (referencia interna) del producto en una columna separada en las facturas de venta'
    )

    show_default_code_quotation = fields.Boolean(
        string='Mostrar código interno en cotizaciones', 
        default=False,
        help='Muestra el código interno (referencia interna) del producto en una columna separada en las cotizaciones'
    )

    show_subtotal_pen = fields.Boolean(
        string='Mostrar subtotales en PEN',
        default=False,
        help='Muestra los subtotales en soles (PEN) al tipo de cambio del día cuando se cotiza en otra moneda'
    )