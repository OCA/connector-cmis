# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
