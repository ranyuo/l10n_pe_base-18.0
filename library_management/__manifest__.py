{
    'name': "Gestión de Biblioteca",
    'version': '18.0.1.0.0',
    'summary': "Un módulo simple para gestionar una colección de libros.",
    'description': """
        Este es un módulo educativo básico para Odoo 18 Enterprise
        que permite al usuario crear y gestionar una lista de libros.
    """,
    'author': "Tu Nombre",
    'website': "https://www.tuweb.com",
    'category': 'Uncategorized',
    'depends': ['base'],
    'data': [
        # El archivo de seguridad se añade aquí, al principio de la lista.
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_address_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}