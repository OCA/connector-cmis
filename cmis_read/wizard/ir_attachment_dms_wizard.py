# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
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
from openerp.tools.translate import _
from openerp.addons.connector.session import ConnectorSession
from ..unit.import_synchronizer import create_doc_from_dms
import logging
_logger = logging.getLogger(__name__)


class ir_attachment_dms_wizard(orm.Model):
    _name = 'ir.attachment.dms.wizard'

    _columns = {
        'name': fields.char('File name', help="File name"),
        'attachment_ids': fields.one2many('ir.attachment.dms', 'wizard_id'),
    }

    def search_doc(self, cr, uid, ids, context=None):
        """
        Search documents from DMS
        """
        if context is None:
            context = {}
        if not ids:
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        ir_attachment_dms_obj = self.pool['ir.attachment.dms']
        record = self.browse(cr, uid, ids, context=context)[0]
        attach_dms_ids = ir_attachment_dms_obj.search(
            cr, uid, [('wizard_id', '=', record.id)], context=context)
        # Empty all data in transient model
        # Because all datas are present each time we do search
        ir_attachment_dms_obj.unlink(cr, uid, attach_dms_ids, context=context)
        if not record.name:
            raise orm.except_orm(_('Error'),
                                 _('You have to fill in the file name. '
                                   'And try again'))

        session = ConnectorSession(cr, uid, context=context)
        file_name = record.name
        search_doc_from_dms(session, 'ir.attachment', file_name, record.id)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment.dms.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': record.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def action_apply(self, cr, uid, ids, context=None):
        """
        Adding documents from DMS to Odoo/OpenERP.
        We just add the data doc
        """
        ir_attachment_dms_obj = self.pool['ir.attachment.dms']
        if context is None:
            context = {}
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        model = context['model']
        res_id = context['ids'][0]
        ir_model_obj = self.pool[context['model']]
        name = ir_model_obj.browse(
            cr, uid, context['ids'], context=context)[0]['name']
        data = self.read(cr, uid, ids, [], context=context)[0]
        session = ConnectorSession(cr, uid, context=context)
        # Just take the lines we select in the tree view
        data['attachment_ids'] = [one_attachment.id for one_attachment in
                                  ir_attachment_dms_obj.browse(
                                      cr, uid, data['attachment_ids'], context)
                                  if one_attachment.selectable_ok]
        if not data['attachment_ids']:
            raise orm.except_orm(_('Error'),
                                 _('You have to select at least 1 Document '
                                   'and try again'))
        # Create doc in Odoo/OpenERP from DMS.
        create_doc_from_dms.delay(session, 'ir.attachment', data, name, model,
                                  res_id, uid)
        return {
            'name': _('Document Page'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': model,
            'view_id': False,
            'res_id': res_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


def search_doc_from_dms(session, model_name, file_name, wizard_id):
    """
    Function to search documents in DMS
    """
    cmis_backend_obj = session.pool.get('cmis.backend')
    ir_attach_dms_obj = session.pool.get('ir.attachment.dms')
    cr = session.cr
    uid = session.uid
    context = session.context
    if context is None:
        context = {}
    # Empty all data in transient model
    # Because all datas are present each time we do search
    attach_dms_ids = ir_attach_dms_obj.search(
        cr, uid, [('wizard_id', '=', wizard_id)], context=context)
    ir_attach_dms_obj.unlink(cr, uid, attach_dms_ids, context=context)
    # List of backend where browsing_ok is True
    ids = cmis_backend_obj.search(
        cr, uid, [('browsing_ok', '=', 'True')], context=context)
    i = 0
    for backend in session.browse('cmis.backend', ids):
        try:
            repo = cmis_backend_obj.check_auth(
                session.cr, session.uid, [backend.id], context=session.context)
            results = cmis_backend_obj.safe_query(
                "SELECT cmis:name, cmis:createdBy, cmis:objectId, "
                "cmis:contentStreamLength FROM cmis:document "
                "WHERE cmis:name LIKE '%%%s%%'", file_name, repo)
            for result in results:
                info = result.getProperties()
                if info['cmis:contentStreamLength'] != 0:
                    data_attach = {
                        'name': info['cmis:name'],
                        'owner': info['cmis:createdBy'],
                        'file_id': info['cmis:objectId'],
                        'wizard_id': wizard_id,
                    }
                session.create('ir.attachment.dms', data_attach)
            i += 1
            break
        except:
            continue
    # Error connection to DMS
    if i == 0:
        raise orm.except_orm(_('CMIS connection Error!'),
                             _("Check your CMIS account configuration."))
