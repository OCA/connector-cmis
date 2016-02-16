# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
