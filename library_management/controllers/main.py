# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class LibraryWebsite(http.Controller):

    @http.route('/biblioteca', type='http', auth='public', website=True)
    def show_books(self, search="", **kwargs):
        """
        Esta función se ejecuta cuando un usuario visita la URL /biblioteca.
        Muestra la lista de libros y maneja la búsqueda.
        """
        # Dominio de búsqueda: busca libros cuyo título contenga el texto de búsqueda.
        # 'ilike' no distingue entre mayúsculas y minúsculas.
        domain = [('name', 'ilike', search)]
        
        # Realizamos la búsqueda en el modelo 'library.book'
        books = request.env['library.book'].search(domain)
        
        # Preparamos los valores que enviaremos a la plantilla
        values = {
            'books': books,
            'search': search, # Para recordar el texto buscado en la caja de búsqueda
        }
        
        # Renderizamos la plantilla y le pasamos los valores
        return request.render('library_management.book_list_template', values)