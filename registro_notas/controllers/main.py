# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class RegistroNotasPortal(http.Controller):

    @http.route(
        ['/registro_notas', '/registro_notas/buscar'],
        type='http',
        auth='public',
        website=True,
        methods=['GET', 'POST'],
        csrf=False,
    )
    def portal_registro_notas(self, **kwargs):
        context = {'records': False, 'student_code': False, 'no_results': False}
        if request.httprequest.method == 'POST':
            student_code = kwargs.get('student_code', '').strip()
            context['student_code'] = student_code
            if student_code:
                records = request.env['registro.nota'].sudo().search([('student_code', '=', student_code)])
                context['records'] = records
                context['no_results'] = not bool(records)
            else:
                context['no_results'] = True
        return request.render('registro_notas.portal_registro_notas', context)
