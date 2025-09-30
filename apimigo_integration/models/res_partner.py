from odoo import models,api
from odoo.addons.apimigo_integration.service.apimigo import ApiMigo
from odoo.exceptions import UserError
import logging
import re
_logger = logging.getLogger(__name__)

patron_ruc = re.compile(r'[12]\d{10}$')
patron_dni = re.compile(r'\d{8}$')

class ResPartner(models.Model):
    _inherit = "res.partner"


    @api.model
    def _api_search_partner_by_vat_apimigo(self,l10n_pe_vat_code,vat):
        result = {}
        ICPSudo = self.env["ir.config_parameter"].sudo()
        apimigo_token = ICPSudo.get_param("apimigo_token", default="")
        
        if l10n_pe_vat_code in ["6","1"]:
            if apimigo_token:
                client = ApiMigo(apimigo_token)
                if l10n_pe_vat_code == "6" and patron_ruc.match(vat or ""):
                    result = client.get_ruc(vat)
                elif l10n_pe_vat_code == "1" and patron_dni.match(vat or ""):
                    result = client.get_dni(vat)
            else:
                raise UserError("El Access Token de APIMIGO no se encuentra establecido.")
        return result


    @api.model
    def _match_partner_ruc_fields(self,vals):
        result = {
            "name":vals.get("nombre_o_razon_social"),
            "street":vals.get("direccion"),
            "street2":vals.get("direccion_simple")
        }

        #Aqui voy a parametrizar otros campos dinámicos como lo son: ubigeo, estado de contribuyente, agente de retension,
        
        return result

    @api.model
    def _process_values_partner_apimigo(self,result_api):
        vals = {}
        if "dni" in result_api:
            vals.update(name = result_api.get("nombre",False))
        elif "ruc" in result_api:
            vals.update(self._match_partner_ruc_fields(result_api))
            
        return vals
        
    @api.model
    def api_search_partner_by_vat_apimigo(self,l10n_pe_vat_code,vat):
        vals = {}
        result_api = self._api_search_partner_by_vat_apimigo(l10n_pe_vat_code,vat)
        if result_api != {}:
            vals = self._process_values_partner_apimigo(result_api)
        return vals
    
    
    @api.onchange('l10n_latam_identification_type_id', 'vat')
    def change_vat(self):
        for record in self:
            record.update(self.api_search_partner_by_vat_apimigo(record.l10n_latam_identification_type_id.l10n_pe_vat_code,record.vat))
