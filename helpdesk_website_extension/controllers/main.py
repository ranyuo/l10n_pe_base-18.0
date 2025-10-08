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
            helpdesk_ticket = HelpdeskTicket.search(domain)

        return request.render("helpdesk_website_extension.helpdesk_ticket_search_page", {
            'helpdesk_ticket': helpdesk_ticket,
            'search': search
        })
