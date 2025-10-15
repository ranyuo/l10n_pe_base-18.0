from odoo import models, fields

class LibraryBook(models.Model):
    """
    Este modelo representa un libro en nuestra biblioteca.
    """
    _name = 'library.book'
    _description = 'Libro de la Biblioteca'

    # --- Definición de los Campos ---
    name = fields.Char(string='Título', required=True)
    author = fields.Char(string='Autor')
    is_available = fields.Boolean(string='Disponible', default=True)