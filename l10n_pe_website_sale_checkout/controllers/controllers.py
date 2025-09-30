from odoo import http,_,tools,SUPERUSER_ID
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
from werkzeug.exceptions import Forbidden, NotFound

from odoo.addons.website_sale.controllers.main import WebsiteSale

import requests
import json
import re
import logging
_logger = logging.getLogger(__name__)


class WebsiteSaleExtend(WebsiteSale):

    WRITABLE_PARTNER_FIELDS = [
        'name',
        'email',
        'phone',
        'street',
        'street2',
        'city',
        'zip',
        'country_id',
        'state_id',
        'city_id',
        'l10n_pe_district',
        'vat',
        'contact_vat',
        'contact_l10n_latam_identification_type_id',
        'require_invoice'
    ]
    
    def _get_mandatory_fields_shipping(self, country_id=False):
        req = super(WebsiteSaleExtend,self)._get_mandatory_fields_shipping(country_id)
        req.append("email")
        
        if "city" in req:
            req.remove("city")
        if "zip" in req:
            req.remove("zip")
        
        if not request.env['website'].get_current_website().show_address_in_checkout:
            if "street" in req: req.remove("street")
            if "country_id" in req: req.remove("country_id")
            if "city_id" in req: req.remove("city_id")
            if "l10n_pe_district" in req: req.remove("l10n_pe_district")
            
        _logger.info("_get_mandatory_fields_shipping")
        _logger.info(req)
        return req
    
    def _get_mandatory_fields_billing(self, country_id=False):
        res = super(WebsiteSaleExtend,self)._get_mandatory_fields_billing()
        res.append("phone")
        
        if request.env['website'].get_current_website().require_identity_document_for_invoice:
            res.append('contact_vat')
            res.append('contact_l10n_latam_identification_type_id')
        
        #res.append('state_id')
        #res.append('city_id')
        #res.append('l10n_pe_district')
        
        if not request.env['website'].get_current_website().show_address_in_checkout:
            res.remove("street")
            res.remove("country_id")
        
        if "city" in res:
            res.remove("city")
            
        if 'vat' in res:
            res.remove("vat")
        
        _logger.info("_get_mandatory_fields_billing")
        _logger.info(res)
        return res


    @http.route(['/list-states-by-country'], type='json', auth="public", website=True)
    def ListStatesByCountry(self, country_id, **kw):
        if country_id:
            return request.env['res.country.state'].sudo().search([('country_id', '=', int(country_id)),('country_id', '!=', False)]).mapped(lambda r: {'id': r.id, 'name':r.name})
        return []
    

    @http.route(['/list-cities-by-state'], type='json', auth="public", website=True)
    def ListCitiesByState(self, state_id, **kw):
        if state_id:
            return http.request.env['res.city'].sudo().search([('state_id', '=', int(state_id)),('state_id', '!=', False)]).mapped(lambda r: {'id': r.id, 'name': r.name})
        return []
        

    @http.route(['/list-districts-by-city'], type='json', auth="public", website=True)
    def ListDistrictsByCity(self, city_id, **kw):
        if city_id:
            return http.request.env['l10n_pe.res.city.district'].sudo().search([('city_id', '=', int(city_id)),('city_id', '!=', False)]).mapped(lambda r: {'id': r.id, 'name': r.name})
        return []


    def values_preprocess(self,values):
        new_values = super().values_preprocess(values)
        new_values.update({'require_invoice' : new_values.get('require_invoice',False) == '1',
                           'company_type' : 'person'})

        return new_values

    def _get_country_related_render_values(self, kw, render_values):
        res = super()._get_country_related_render_values(kw, render_values)
        if request.website.sudo().company_id.country_id.code == "PE":
            res.update({
                'state_cities': request.env['res.city'].sudo().search([]),
                'city_disctrits': request.env['l10n_pe.res.city.district'].sudo().search([]),
            })
        return res