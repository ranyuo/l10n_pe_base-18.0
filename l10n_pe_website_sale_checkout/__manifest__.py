{
    'name': 'Website Sale - Checkout',
    'author': 'Daniel Moreno <daniel@codlan.com>',
    'countries': ['pe'],
    'version': '1.0',
    'license': 'OPL-1',
    'website': 'https://www.codlan.com',
    'depends': [
        'base','account','sale','website','website_sale','l10n_pe',"l10n_pe_partner"
    ],
    'data': [
        'data/function.xml',
        'views/checkout_form.xml',
        'views/l10n_latam_identification_type.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/checkout_layout.xml',
        'views/payment_confirmation_status.xml',
        'views/website.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'l10n_pe_website_sale_checkout/static/src/js/checkout.js',
        ]
    },
}