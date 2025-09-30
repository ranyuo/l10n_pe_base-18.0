{
    "name":"Generación de XML y métodos de recuperación de XML",
    "summary":"Módulo con clases para la generación de XML y recuperación de CDR para los documentos: Factura, Boleta, Notas asociadas, Anulación, Resumen diario",
    "depends":[
        "base",
        "base_setup",
        "base_automation",
        "sale",
        "account",
        "account_edi",
        "l10n_latam_invoice_document",
        "l10n_pe",
        "l10n_pe_edi",
        "l10n_pe_edi_stock",
        "l10n_pe_reports",
        "l10n_pe_reports_stock",
        "l10n_pe_reports_stock_extend",
        "account_edi_ubl_cii",
    ],
    "author":"Daniel Moreno <daniel@codlan.com>",
    "countries": ["pe"],
    "version": "1.0",
    "website": "https://www.codlan.com",
    "data": [
        "security/ir_model_access.xml",
        "data/l10n_pe_ubl.xml",
        "data/l10n_pe_edi_stock.xml",
        "data/account_tax.xml",
        "data/automation.xml",
        "views/view_res_company.xml",
        "views/view_account_move.xml",
        "views/view_account_tax.xml",
        "views/view_sale_order.xml",
        "views/view_res_partner_bank.xml",
        "views/view_stock_picking.xml",
        "views/view_res_partner.xml",
        "views/view_product_template.xml",
        "templates/report_invoice_document.xml",
        "templates/report_saleorder_document.xml",
        "templates/report_stock_picking.xml",
        "templates/l10n_pe_report_invoice_document.xml"
    ],
    "installable": True,
    "license":"OPL-1"
}



