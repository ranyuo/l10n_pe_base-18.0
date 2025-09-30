{
    "name":"Ventas - Campo Vendedor",
    "version":"1.0",
    "license":"OPL-1",
    "summary":"Agrega campo de vendedor personalizado en órdenes de venta y facturas",
    "description":"""
    Ventas - Campo Vendedor
    =======================
    
    Este módulo agrega funcionalidad para gestionar un campo de vendedor personalizado 
    en las órdenes de venta y facturas de Odoo.
    
    Características:
    ----------------
    * Campo vendedor en órdenes de venta
    * Campo vendedor en facturas (account.move)
    * Integración con reportes automática
    * Validación de dominio (solo contactos marcados como vendedores)
    * Datos del vendedor disponibles en data_report()
    
    Datos disponibles en reportes:
    * salesman_name: Nombre del vendedor
    * salesman_email: Email del vendedor
    * salesman_mobile: Teléfono móvil del vendedor
    """,
    "author":"Daniel Moreno <daniel@codlan.com>",
    "depends":[
        "base",
        "sale",
        "sale_management",
        "external_layout_header_compact"
    ],
    "data":[
        "views/sale_order.xml",
        "views/res_partner.xml",
        "views/sale_report.xml",
        "views/account_move.xml",
        "views/account_invoice_report.xml",
        "templates/report_saleorder_document.xml"
    ]
}