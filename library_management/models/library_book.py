from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Libro de la Biblioteca'

    name = fields.Char(string='Título', required=True)
    author = fields.Char(string='Autor')
    is_available = fields.Boolean(string='Disponible', default=True)

    # --- CAMPO AÑADIDO ---
    # Este campo crea la relación con el modelo 'library.address'.
    # Odoo automáticamente creará un selector desplegable.
    address_id = fields.Many2one(
        'library.address', 
        string='Ubicación'
    )