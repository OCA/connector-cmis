# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class CmisImportMapper(ImportMapper):

    @mapping
    def cmis_backend_id(self, record):
        return {'cmis_backend_id': self.backend_record.id}

    @mapping
    def updated_on(self, record):
        date = record['updated_on']
        return {'updated_on': date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)}

    @mapping
    def sync_date(self, record):
        date = datetime.now()
        return {'sync_date': date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)}
