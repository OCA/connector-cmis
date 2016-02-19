# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from cmislib.model import CmisClient
import cmislib.exceptions
from cmislib.browser.binding import BrowserBinding
import urllib2

from openerp.tools.translate import _
from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from openerp.addons.cmis.exceptions import CMISConnectionError


class CmisAdapter(CRUDAdapter):

    def _auth(self, cmis_backend):
        """Test connection with CMIS"""
        cmis_backend.ensure_one()
        client = CmisClient(
            cmis_backend.location,
            cmis_backend.username,
            cmis_backend.password,
            binding=BrowserBinding())

        try:
            return client.defaultRepository
        except cmislib.exceptions.ObjectNotFoundException:
            raise CMISConnectionError(
                _("Check your CMIS account configuration."))
        except cmislib.exceptions.PermissionDeniedException:
            raise CMISConnectionError(
                _("Check your CMIS account configuration."))
        except urllib2.URLError:
            raise CMISConnectionError(
                _("SERVER is down."))
