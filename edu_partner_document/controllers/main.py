from odoo import http
from odoo.http import request
import math

import logging
_logger = logging.getLogger(__name__)


class WebsitePartnerDocument(http.Controller):

    @http.route(['/partner-document', '/partner-document/page/<int:page>'], type='http', auth="public", website=True)
    def partner_document_list(self, page=1, **kwargs):
        search = kwargs.get('search', '')
        domain = []

        if search:
            domain = ['|','|', ('name', 'ilike', search), ('partner_code', '=', search), ('partner_vat', '=', search)]

        page_size = 10
        PartnerDocument = request.env['edu.partner.document'].sudo()
        total = PartnerDocument.search_count(domain)
        pages = math.ceil(total / page_size)

        offset = (page - 1) * page_size
        partner_documents = PartnerDocument.search(domain, limit=page_size, offset=offset)

        return request.render("edu_partner_document.partner_document_page", {
            'partner_documents': partner_documents,
            'search': search,
            'page': page,
            'pages': pages,
            'total': total,
        })
