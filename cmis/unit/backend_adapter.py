# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 - Present Savoir-faire Linux
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.tools.translate import _
from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
import cmislib.exceptions
from cmislib.model import CmisClient
import urllib2


class CmisAdapter(CRUDAdapter):

    def _auth(self, ids):
        """Test connection with CMIS"""
        if type(ids) is not list:
            ids = [ids]
        # Get the url, user and password for CMIS
        # ids = self.search(cr, uid, [])
        if not ids:
            raise orm.except_orm(
                _('Internal Error'),
                _('Something very wrong happened. _auth() '
                    'called without any ids.')
            )
        res = self.backend_record.read(['location', 'username', 'password'])[0]
        url = res['location']
        user_name = res['username']
        user_password = res['password']
        client = CmisClient(url, user_name, user_password)

        try:
            return client.defaultRepository
        except cmislib.exceptions.ObjectNotFoundException:
            raise orm.except_orm(_('CMIS connection Error!'),
                                 _("Check your CMIS account configuration."))
        except cmislib.exceptions.PermissionDeniedException:
            raise orm.except_orm(_('CMIS connection Error!'),
                                 _("Check your CMIS account configuration."))
        except urllib2.URLError:
            raise orm.except_orm(_('CMIS connection Error!'),
                                 _("SERVER is down."))
