# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CMIS Write',
    'version': '9.0.1.0.0',
    'category': 'Knowledge Management',
    'summary': 'Create Document in DMS from Odoo/OpenERP',
    'author': 'Savoir-faire Linux, Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': [
        'document',
        'cmis',
    ],
    'data': [
        'views/document_view.xml',
        'views/metadata_view.xml',
        'security/ir.model.access.csv',
    ],
    'js': [
        'static/src/js/document.js'
    ],
    'qweb': [],
    'test': [],
    'demo': [],
    'installable': False,
    'auto_install': False,
}
