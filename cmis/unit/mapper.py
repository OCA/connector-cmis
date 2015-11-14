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

from openerp.addons.connector.unit.mapper import ImportMapper, mapping
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class CmisImportMapper(ImportMapper):

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def updated_on(self, record):
        date = record['updated_on']
        return {'updated_on': date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)}

    @mapping
    def sync_date(self, record):
        date = datetime.now()
        return {'sync_date': date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)}
