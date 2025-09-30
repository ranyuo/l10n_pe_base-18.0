{
    'name': 'Contabilidad de Retenciones en Comprobantes de Venta',
    'version': '1.0',
    'license': 'OPL-1',
    'summary': "Contabilidad de Retenciones en Comprobantes de Venta",
    'author': "Franco Najarro",
    'website': '',
    'depends': [
        'base',
        'base_setup',
        'account',
        'l10n_pe_account_document_extra_fields',
        'l10n_pe_edi_doc'],
    'data': [
        'data/journal_data.xml',
        'data/ir_config_parameter.xml',
        'security/ir.model.access.csv',
        'views/account_journal_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/wizard_paid_retention_view.xml',
        'views/account_move_view.xml',
        'views/account_invoice_retention_view.xml',
        'views/res_config_settings_view.xml',
        ],
    'installable': True,
    'auto_install': True
}
