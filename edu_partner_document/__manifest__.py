{
    'name': 'Registro documental para contactos',
    'version': '18.1.0',
    'description': 'Registra documentos asociados a contactos',
    'summary': '',
    'author': 'Christian Bravo',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'website'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/edu_document_type_views.xml",
        "views/edu_educational_institution_views.xml",
        "views/edu_partner_document_views.xml",
        "views/menuitem.xml",
        "templates/edu_partner_document.xml"
    ],
    'auto_install': False,
    'application': False,
    # 'assets': {
        
    # }
}