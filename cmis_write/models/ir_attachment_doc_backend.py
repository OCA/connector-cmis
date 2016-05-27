# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class IrAttachmentDocBackend(models.Model):
    _description = "List of backend's document"
    _name = 'ir.attachment.doc.backend'

    attachment_id = fields.Many2one(
        'ir.model.fields',
        'Document',
        ondelete='cascade',
        help="Document"
    )
    cmis_backend_id = fields.Many2one(
        'cmis.backend',
        'Backend',
        ondelete='cascade',
        help="Backend",
        oldname='backend_id'
    )
    object_doc_id = fields.Char(
        "Id of document backend",
        help="Id of document backend"
    )
