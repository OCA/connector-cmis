# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'CMIS',
    'version': '7.0.1.1.0',
    'category': 'Connector',
    'summary': 'Connect OpenERP with a CMIS server',
    'description': """
CMIS Connector
==============

This module is the base for OpenERP modules implementing different integration
scenario with a CMIS server.
It allows you to configure a CMIS backend in OpenERP.

Configuration
=============

Create a new CMIS backend with the host, login and password.

Contributors
------------
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
* Maxime Chambreuil (maxime.chambreuil@savoirfairelinux.com)
""",
    'author': "Savoir-faire Linux, Odoo Community Association (OCA)",
    'website': 'www.savoirfairelinux.com',
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
    ],
    'installable': True,
    'auto_install': False,
}
