from odoo import http
from odoo.http import request
import math

import logging
_logger = logging.getLogger(__name__)


class WebsiteHelpdeskTicket(http.Controller):

    @http.route(['/helpdesk-ticket-search'], type='http', auth="public", website=True)
    def helpdesk_ticket_search(self, **kwargs):
        search = kwargs.get('search', '')
        domain = []
        helpdesk_ticket = []

        if search:
            domain = [('ticket_ref', '=', search)]
            HelpdeskTicket = request.env['helpdesk.ticket'].sudo()
            helpdesk_ticket = HelpdeskTicket.search(domain, limit=1)

        return request.render("helpdesk_website_extension.helpdesk_ticket_search_page", {
            'helpdesk_ticket': helpdesk_ticket,
            'search': search
        })

    @http.route(
        '/helpdesk-ticket/<int:ticket_id>/print',
        type='http',
        auth="public",
        website=True,
    )
    def helpdesk_ticket_print(self, ticket_id, **kwargs):
        HelpdeskTicket = request.env['helpdesk.ticket'].sudo()
        ticket = HelpdeskTicket.browse(ticket_id)
        if not ticket.exists():
            return request.not_found()

        return request.render(
            "helpdesk_website_extension.helpdesk_ticket_print_page",
            {
                'helpdesk_ticket': ticket,
            },
        )

    @http.route(
        '/helpdesk-ticket/<int:ticket_id>/pdf',
        type='http',
        auth="public",
        website=True,
    )
    def helpdesk_ticket_pdf(self, ticket_id, **kwargs):
        HelpdeskTicket = request.env['helpdesk.ticket'].sudo()
        ticket = HelpdeskTicket.browse(ticket_id)
        if not ticket.exists():
            return request.not_found()

        report = request.env.ref('helpdesk_website_extension.action_report_helpdesk_ticket').sudo()
        pdf_content, _ = report._render_qweb_pdf([ticket.id])

        filename = "Expediente-%s" % (ticket.ticket_ref or ticket.name or ticket.id)
        filename = str(filename).replace('/', '-').replace('\\', '-')

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            (
                'Content-Disposition',
                'attachment; filename="%s.pdf"' % filename,
            ),
        ]

        return request.make_response(pdf_content, headers=pdfhttpheaders)
