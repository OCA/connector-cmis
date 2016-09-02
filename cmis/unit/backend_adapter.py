# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from cmislib.model import CmisClient
import cmislib.exceptions
from cmislib.browser.binding import BrowserBinding
import urllib2
import logging

from openerp.tools.translate import _
from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from openerp.addons.cmis.exceptions import CMISConnectionError

logger = logging.getLogger(__name__)


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
            logger.exception("CMIS backend not found")
            raise CMISConnectionError(
                _("CMIS backend not found.\n"
                  "Check your CMIS account configuration."))
        except cmislib.exceptions.PermissionDeniedException:
            logger.exception("Permission denied")
            raise CMISConnectionError(
                _("Permission denied.\n"
                  "Check your CMIS account configuration."))
        except urllib2.URLError:
            logger.exception("UrlError")
            raise CMISConnectionError(
                _("SERVER is down."))
