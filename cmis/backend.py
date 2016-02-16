# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.addons.connector.backend as backend


cmis = backend.Backend('cmis')
""" Generic CMIS Backend """

cmis1000 = backend.Backend(parent=cmis, version='1.0')
""" CMIS Backend for version 1.0 """
