# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class ir_attachment_download(orm.TransientModel):
    _name = 'ir.attachment.download'

    _columns = {
        'name': fields.char(
            'Attachment Name',
            required=True,
            help='Attachment Name'
        ),
        'datas': fields.binary('File', readonly=True),
        'type': fields.char('Type', help='Type'),
        'file_type': fields.char('Content Type', help='Content Type'),
        'attachment_id': fields.many2one(
            'ir.attachment',
            'Attachment',
            help="Attachment"
        ),
    }
    _defaults = {
        'type': 'binary',
    }
