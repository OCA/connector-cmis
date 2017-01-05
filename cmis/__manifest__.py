# -*- coding: utf-8 -*-

# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CMIS',
    'version': '10.0.1.0.0',
    'category': 'Connector',
    'summary': 'Connect OpenERP with a CMIS server',
    'author': "Savoir-faire Linux, "
              "ACSONE SA/NV, "
              "Odoo Community Association (OCA)",
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'external_dependencies': {
        'python': ['cmislib'],
    },
    'data': [
        'security/cmis_backend.xml',
        'views/cmis_menu.xml',
        'views/cmis_backend.xml',
    ],
    'demo': [
        'demo/cmis_backend_demo.xml',
    ],
    'installable': True,
}
