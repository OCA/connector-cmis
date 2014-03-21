# -*- coding: utf-8 -*-
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


class ir_attachment_dms(orm.TransientModel):
    _name = 'ir.attachment.dms'

    _columns = {
        'name': fields.char('Title',
                            readonly=True,
                            help="File name"),
        'code': fields.char('Code',
                            readonly=True,
                            help="File name"),
        'file_id': fields.char('File ID',
                               readonly=True,
                               help="File Id"),
        'wizard_id': fields.many2one('ir.attachment.dms.wizard',
                                     string='Wizard',
                                     required=True),
        'selectable_ok': fields.boolean('Selected', help="Selected."),
    }
