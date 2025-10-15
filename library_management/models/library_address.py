from odoo import models, fields

class LibraryAddress(models.Model):
    """
    Este modelo representa la dirección de una sede de la biblioteca.
    """
    _name = 'library.address'
    _description = 'Dirección de Biblioteca'

    # --- Definición de los Campos ---

    # El nombre de la sede, por ejemplo: "Sede Central", "Sucursal Norte".
    name = fields.Char(string='Nombre de la Sede', required=True)
    
    street = fields.Char(string='Calle y Número')
    city = fields.Char(string='Ciudad')
    
    # Este es un campo relacional. Nos permite seleccionar un país
    # de la lista de países que ya existen en Odoo.
    # El modelo 'res.country' contiene todos los países del mundo.
    country_id = fields.Many2one('res.country', string='País')