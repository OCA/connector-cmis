# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class IrAttachmentDownload(models.TransientModel):
    _name = 'ir.attachment.download'

    name = fields.Char(
        'Attachment Name', required=True, help='Attachment Name')
    datas = fields.Binary('File', readonly=True)
    type = fields.Char(default='binary')
    file_type = fields.Char('Content Type', help='Content Type')
    attachment_id = fields.Many2one(
        'ir.attachment', 'Attachment', help="Attachment"
    )
