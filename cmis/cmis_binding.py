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

from openerp.osv import orm, fields


class CmisBinding(orm.AbstractModel):
    _name = 'cmis.binding'
    _inherit = 'external.binding'
    _description = 'DMS Binding (Abstract)'

    _columns = {
        'backend_id': fields.many2one(
            'cmis.backend', 'CMIS Backend', required=True,
            ondelete='restrict'
        ),
        'dms_id': fields.integer('ID in Dms', required=True),
        'sync_date': fields.datetime(
            'Last Synchronization Date', required=True),
        'updated_on': fields.datetime('Last Update in Dms')

    }
