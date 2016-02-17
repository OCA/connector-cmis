# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class metadata_list(orm.Model):
    _description = 'List of Metadata'
    _name = 'metadata.list'

    _columns = {
        'field_id': fields.many2one(
            'ir.model.fields',
            'Fields',
            help="Fields"
        ),
        'metadata_id': fields.many2one(
            'metadata',
            'Metadata',
            help="Metadata"
        ),
    }
