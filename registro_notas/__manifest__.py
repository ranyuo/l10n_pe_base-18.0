# -*- coding: utf-8 -*-
{
    'name': 'Registro de Notas',
    'version': '1.0.0',
    'summary': 'Permite registrar y consultar notas de alumnos.',
    'sequence': 10,
    'license': 'LGPL-3',
    'author': 'Custom',
    'category': 'Education',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/registro_nota_views.xml',
        'views/registro_maestro_views.xml',
        'views/registro_nota_menu.xml',
        'views/registro_nota_templates.xml',
    ],
    'installable': True,
    'application': True,
}
