# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class CmisBinding(models.AbstractModel):
    _name = 'cmis.binding'
    _inherit = 'external.binding'
    _description = 'DMS Binding (Abstract)'

    cmis_backend_id = fields.Many2one(
        'cmis.backend', 'CMIS Backend', required=True,
        ondelete='restrict', oldname='backend_id')
    dms_id = fields.Integer('ID in Dms', required=True)
    sync_date = fields.Datetime(
        'Last Synchronization Date', required=True)
    updated_on = fields.Datetime('Last Update in Dms')
