# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class LibraryWebsite(http.Controller):

    @http.route('/biblioteca', type='http', auth='public', website=True)
    def show_books(self, search="", **kwargs):
        """
        Esta función ahora solo busca libros si se proporciona un término de búsqueda.
        """
        # Inicializamos la lista de libros como una lista vacía.
        books = []
        
        # --- LÓGICA MODIFICADA ---
        # Solo si el usuario ha escrito algo en la caja de búsqueda...
        if search:
            # ...realizamos la búsqueda en la base de datos.
            domain = [('name', 'ilike', search)]
            books = request.env['library.book'].search(domain)
        
        # Preparamos los valores que enviaremos a la plantilla.
        # 'books' estará vacío en la carga inicial, o lleno si hubo una búsqueda.
        values = {
            'books': books,
            'search': search,
        }
        
        # Renderizamos la plantilla como antes.
        return request.render('library_management.book_list_template', values)