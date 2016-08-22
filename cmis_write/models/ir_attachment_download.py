# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
