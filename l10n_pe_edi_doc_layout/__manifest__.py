{
    "name":"(obsoleto) Mejoras en layout de comprobantes de Venta en formato electrónico.",
    'version': '2.0',
    'license':'OPL-1',
    "summary":"Mejoras en layout de comprobantes de Venta en formato electrónico",
    "depends":[
        "base",
        "account",
        "l10n_pe_edi",
        "l10n_pe_edi_doc",
        "l10n_pe_retentions"
    ],
    "countries": ["pe"],
    "data": [
    	"views/account_move_view.xml",
        "views/report_invoice_document.xml",
    ],
    'auto_install': False,
}