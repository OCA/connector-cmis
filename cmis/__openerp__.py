# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CMIS',
    'version': '9.0.1.0.0',
    'category': 'Connector',
    'summary': 'Connect OpenERP with a CMIS server',
    'author': "Savoir-faire Linux, Odoo Community Association (OCA)",
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': [
        'connector',
    ],
    'external_dependencies': {
        'python': ['cmislib'],
    },
    'data': [
        'views/cmis_backend_view.xml',
        'views/cmis_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
