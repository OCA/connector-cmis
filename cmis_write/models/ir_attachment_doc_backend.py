# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class ir_attachment_doc_backend(orm.Model):
    _description = "List of backend's document"
    _name = 'ir.attachment.doc.backend'

    _columns = {
        'attachment_id': fields.many2one(
            'ir.model.fields',
            'Document',
            ondelete='cascade',
            help="Document"
        ),
        'backend_id': fields.many2one(
            'cmis.backend',
            'Backend',
            ondelete='cascade',
            help="Backend"
        ),
        'object_doc_id': fields.char(
            "Id of document backend",
            help="Id of document backend"
        ),
    }
