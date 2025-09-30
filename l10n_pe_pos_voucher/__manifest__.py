{
    "name":"Voucher Number from Point of Sale",
    "author":"CodLan, Harrison Chumpitaz",
    "category": "Accounting/Localizations/Point of Sale",
    "version": "1.0",
    "website": "https://www.codlan.com",
    "depends":[
        "l10n_pe_edi",
        "point_of_sale",
        "l10n_pe_pos_base",
    ],
    "license": "OPL-1",
    "countries": ["pe"],
    "data": [
        "views/pos_order_views.xml",
        "views/pos_payment_views.xml"
    ],
    "installable": True,
    "assets": {
        "point_of_sale._assets_pos": [
            "l10n_pe_pos_voucher/static/src/**/*"
        ],
    },
}