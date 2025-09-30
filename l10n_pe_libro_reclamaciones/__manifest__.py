{
    'name': 'Libro de Reclamaciones',
    'summary': 'Libro de Reclamaciones digital para Odoo, cumpliendo normativa peruana.',
    'version': '1.0',
    'category': 'Localization',
    'author': 'Codlan, Daniel Moreno',
    'website': 'https://codlan.com',
    'license':'OPL-1',
    'support': 'daniel@codlan.com',
    'description': '''\
Este módulo implementa un sistema completo de Libro de Reclamaciones para Odoo, permitiendo a los clientes registrar reclamos y quejas a través del sitio web y a la empresa gestionarlos desde el backend, cumpliendo con la normativa peruana. Incluye formulario web, gestión interna, notificaciones automáticas, reportes PDF y configuración avanzada.
''',
    'depends': ['base','base_automation','l10n_pe','mail','website'],
    'images':['images/main_screenshot.png'],
    'data': [
        'security/security.xml',
        'data/ir_sequence.xml',
        'report/libro_reclamaciones_template.xml',
        'report/report.xml',
        'data/mail_template.xml',
        'data/automation.xml',
        'views/views.xml',
        'views/res_config_settings.xml',
        'templates/libro_reclamaciones.xml',
     ],
    "assets": {
        "web.assets_frontend": [
            "l10n_pe_libro_reclamaciones/static/src/js/libro_reclamacion.js",
        ]
    },
    'application': True,
    'installable': True,
    'auto_install': False
}
