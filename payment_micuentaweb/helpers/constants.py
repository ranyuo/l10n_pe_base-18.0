# coding: utf-8
#
# Copyright © Lyra Network.
# This file is part of Izipay plugin for Odoo. See COPYING.md for license details.
#
# Author:    Lyra Network (https://www.lyra.com)
# Copyright: Copyright © Lyra Network
# License:   http://www.gnu.org/licenses/agpl.html GNU Affero General Public License (AGPL v3)

from odoo import _

# WARN: Do not modify code format here. This is managed by build files.
MICUENTAWEB_PLUGIN_FEATURES = {
    'multi': False,
    'restrictmulti': False,
    'qualif': False,
    'shatwo': True,
}

MICUENTAWEB_PARAMS = {
    'GATEWAY_CODE': 'Mi_Cuenta_Web',
    'GATEWAY_NAME': 'Izipay',
    'BACKOFFICE_NAME': 'Izipay',
    'SUPPORT_EMAIL': 'soporte@micuentaweb.pe',
    'GATEWAY_URL': 'https://secure.micuentaweb.pe/vads-payment/',
    'SITE_ID': '12345678',
    'KEY_TEST': '1111111111111111',
    'KEY_PROD': '2222222222222222',
    'CTX_MODE': 'TEST',
    'SIGN_ALGO': 'SHA-256',
    'LANGUAGE': 'es',

    'GATEWAY_VERSION': 'V2',
    'PLUGIN_VERSION': '4.0.0',
    'CMS_IDENTIFIER': 'Odoo_17',
}

MICUENTAWEB_LANGUAGES = {
    'cn': 'Chinese',
    'de': 'German',
    'es': 'Spanish',
    'en': 'English',
    'fr': 'French',
    'it': 'Italian',
    'jp': 'Japanese',
    'nl': 'Dutch',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'sv': 'Swedish',
    'tr': 'Turkish',
}

MICUENTAWEB_CARDS = {
    'MAESTRO': u'Maestro',
    'MASTERCARD': u'Mastercard',
    'VISA': u'Visa',
    'VISA_ELECTRON': u'Visa Electron',
    'VPAY': u'V PAY',
    'AMEX': u'American Express',
    'CENCOSUD': u'Cencosud',
    'DINERS': u'Diners',
    'MASTERCARD_DEBIT': u'Mastercard Débito',
    'OH': u'OH !',
    'PAGOEFECTIVO': u'PagoEfectivo',
    'RIPLEY': u'Ripley',
    'VISA_DEBIT': u'Visa Débito',
}

MICUENTAWEB_CURRENCIES = [
    ['PEN', '604', 2],
    ['USD', '840', 2],
]

MICUENTAWEB_ONLINE_DOC_URI = {
    'es': 'https://secure.micuentaweb.pe/doc/es-PE/plugins/',
}

MICUENTAWEB_DOCUMENTATION = {
    'fr': 'Français',
    'en': 'English',
    'es': 'Español',
    'de': 'Deutsch',
    'pt': 'Português',
}