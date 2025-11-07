from odoo import http
from odoo.http import request
import math
import random

import logging
_logger = logging.getLogger(__name__)


class WebsitePartnerDocument(http.Controller):

    def _get_captcha(self, force_new=False):
        """Return captcha data stored in the session."""
        captcha = request.session.get('partner_document_captcha')
        if force_new or not captcha:
            captcha = self._generate_captcha()
        return captcha

    def _generate_captcha(self):
        number_1 = random.randint(1, 9)
        number_2 = random.randint(1, 9)
        captcha = {
            'question': f"{number_1} + {number_2} = ?",
            'answer': str(number_1 + number_2),
        }
        request.session['partner_document_captcha'] = captcha
        request.session.modified = True
        return captcha

    @http.route(['/partner-document', '/partner-document/page/<int:page>'], type='http', auth="public", website=True)
    def partner_document_list(self, page=1, **kwargs):
        search = (kwargs.get('search') or '').strip()
        domain = []
        partner_documents = []
        pages = 1
        total = 0
        model_missing = False

        captcha_error = False
        captcha_data = self._get_captcha()
        captcha_question = captcha_data.get('question')

        validated_data = request.session.get('partner_document_captcha_validated')
        validated_search = None
        if isinstance(validated_data, dict):
            validated_search = validated_data.get('value')

        if not search:
            if 'partner_document_captcha_validated' in request.session:
                request.session.pop('partner_document_captcha_validated', None)
                request.session.modified = True

        if search:
            captcha_valid = validated_search == search
            if not captcha_valid:
                captcha_answer = (kwargs.get('captcha_answer') or '').strip()
                expected_answer = captcha_data.get('answer')
                captcha_valid = bool(captcha_answer and expected_answer and captcha_answer == expected_answer)
                if captcha_valid:
                    request.session['partner_document_captcha_validated'] = {'value': search}
                    request.session.modified = True
                else:
                    captcha_error = True

            if captcha_valid:
                domain = ['|', '|', '|',
                          ('name', 'ilike', search),
                          ('partner_id.name', 'ilike', search),
                          ('partner_code', 'ilike', search),
                          ('partner_vat', 'ilike', search)]

                page_size = 10

                try:
                    PartnerDocument = request.env['edu.partner.document'].sudo()
                except KeyError:
                    model_missing = True
                    _logger.exception("Model edu.partner.document not available in registry")
                else:
                    total = PartnerDocument.search_count(domain)
                    pages = math.ceil(total / page_size) or 1

                    offset = (page - 1) * page_size
                    partner_documents = PartnerDocument.search(domain, limit=page_size, offset=offset)

            captcha_data = self._get_captcha(force_new=True)
            captcha_question = captcha_data.get('question')

        return request.render("edu_partner_document.partner_document_page", {
            'partner_documents': partner_documents,
            'search': search,
            'page': page,
            'pages': pages,
            'total': total,
            'model_missing': model_missing,
            'captcha_question': captcha_question,
            'captcha_error': captcha_error,
        })
