{
	'name': 'Campos adicionales en Asientos y Apuntes Contables. Pagos/Cobros con Cuenta destino manual',
	'version': "2.1",
 	"license": "OPL-1",
	'author': 'Franco Najarro',
	'website':'https://codlan.com',
	'depends':[
		'base',
  		'base_automation',
		'sale',
		'purchase',
		'account',
		'l10n_pe_edi',
		'l10n_latam_invoice_document',
		'l10n_pe_catalogs_sunat',
		'l10n_pe_payment_method_sunat',
    ],
	'description':'''
		Campos adicionales en Asientos y Apuntes Contables. Pagos/Cobros con Cuenta destino manual
			> Campos adicionales en Asientos y Apuntes Contables. Pagos/Cobros con Cuenta destino manual
		''',
	'data':[
		'automation/account_move.xml',
  		'security/res_groups.xml',
		'views/account_journal_view.xml',
		'views/account_move_view.xml',
		'views/account_move_line_view.xml',        
		'views/account_payment_view.xml',
		'views/account_payment_register_view.xml',
	],
	'installable': True,
	'auto_install': True,
}