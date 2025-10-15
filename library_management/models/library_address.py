from odoo import models, fields

class LibraryAddress(models.Model):
    _name = 'library.address'
    _description = 'Dirección de Biblioteca'

    name = fields.Char(string='Nombre de la Sede', required=True)
    street = fields.Char(string='Calle y Número')
    city = fields.Char(string='Ciudad')
    country_id = fields.Many2one('res.country', string='País')

    # --- CAMPO AÑADIDO (RELACIÓN INVERSA) ---
    # Este campo crea la relación inversa. No se almacena en la base de datos,
    # sino que busca en 'library.book' todos los registros que apunten a esta dirección.
    book_ids = fields.One2many(
        comodel_name='library.book',  # El modelo en el otro extremo de la relación
        inverse_name='address_id',   # El campo 'Many2one' que creamos en el otro modelo
        string='Libros en esta Sede'
    )