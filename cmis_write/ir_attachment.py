# -*- encoding: utf-8 -*-
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

from openerp.osv import orm, osv, fields
from openerp.addons.connector.session import ConnectorSession
from openerp.addons.connector.queue.job import job
import base64
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
from openerp.tools import ustr

import logging
_logger = logging.getLogger(__name__)


class ir_attachment(orm.Model):
    _inherit = 'ir.attachment'

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        metadata_obj = self.pool['metadata']
        user_obj = self.pool['res.users']
        user_login = user_obj.browse(cr, uid, uid, context=context).login
        session = ConnectorSession(cr, uid, context=context)
        value = {}
        if values.get('datas'):
            values['file_type'], values['index_content'] = self._index(
                cr, uid, values['datas'],
                values.get('datas_fname', False), None)
            # Get the extension file
            ext = ''
            if values['file_type']:
                ext = '.' + values['file_type'][values['file_type'].find('/')
                                                + 1:]
            if not values.get('datas_fname'):
                values['datas_fname'] = values.get('name') + ext
            value = {
                'name': values.get('name'),
                'datas_fname': values.get('datas_fname'),
                'datas': values.get('datas'),
                'res_id': values.get('res_id'),
                'res_model': values.get('res_model'),
            }
        metadata_ids = metadata_obj.search(cr, SUPERUSER_ID, [],
                                           context=context)
        dict_metadata = {}
        list_fields = []
        # Get list of metadata
        if values.get('res_model'):
            for line in metadata_obj.browse(cr, SUPERUSER_ID, metadata_ids,
                                            context=context):
                if line.model_id.model == values.get('res_model') and \
                        line.metadata_list_ids:
                    list_fields += [one_field.field_id.name
                                    for one_field in line.metadata_list_ids]
        if list_fields:
            result = self.pool.get(values.get('res_model')).read(cr, uid, [
                values.get('res_id')], list_fields, context=context)[0]
            for one_field in list_fields:
                dict_metadata['cmis:' + one_field] = result[one_field]
        # Don't save the document in Odoo/OpenERP
        values['datas'] = None
        # Create an ir.attachment
        res = super(ir_attachment, self).create(
            cr, uid, values, context=context)
        # if bool_testdoc in context, we don't need to create
        # the doc in the DMS
        if not context.get('bool_testdoc'):
            try:
                create_doc_in_edm(
                    session, 'ir.attachment', value, res, dict_metadata,
                    user_login)

            except (orm.except_orm, osv.except_osv):
                self.unlink(
                    cr, SUPERUSER_ID, res, context=context
                )
                raise

            except Exception as e:
                self.unlink(
                    cr, uid, res, context=context
                )
                raise orm.except_orm(
                    _('Error!'),
                    _('Cannot save the attachment in DMS.') + '\n' + ustr(e)
                )
        return res

    def write(self, cr, uid, ids, values, context=None):
        if context is None:
            context = {}
        metadata_obj = self.pool['metadata']
        user_obj = self.pool['res.users']
        user_login = user_obj.browse(cr, uid, uid, context=context).login
        session = ConnectorSession(cr, uid, context=context)
        if values.get('datas'):
            values['file_type'], values['index_content'] = self._index(
                cr, uid, values['datas'],
                values.get('datas_fname', False), None)
        metadata_ids = metadata_obj.search(
            cr, SUPERUSER_ID, [], context=context
        )
        dict_metadata = {}
        list_fields = []
        # Get list of metadata
        if values.get('res_model'):
            for line in metadata_obj.browse(cr, SUPERUSER_ID, metadata_ids,
                                            context=context):
                if line.model_id.model == values.get('res_model') and \
                        line.metadata_list_ids:
                    list_fields += [one_field.field_id.name
                                    for one_field in line.metadata_list_ids]
        if list_fields:
            result = self.pool.get(values.get('res_model')).read(cr, uid, [
                values.get('res_id')], list_fields, context=context)[0]
            for one_field in list_fields:
                dict_metadata['docubase:' + one_field] = result[one_field]
        # Don't save the document in Odoo/OpenERP
        values['datas'] = None
        res = super(ir_attachment, self).write(cr, SUPERUSER_ID, ids,
                                               values, context=context)
        # TODO: Define this method below
        #update_doc_in_edm(session, 'ir.attachment', ids,
        #                  dict_metadata, user_login)
        return res

    def action_download(self, cr, uid, ids, context=None):
        """
        Download document if it is available in one of backend
        """
        if context is None:
            context = {}
        cmis_backend_obj = self.pool['cmis.backend']
        # login with the cmis account
        backend_ids = cmis_backend_obj.search(cr, uid,
                                              [('storing_ok', '=', 'True')],
                                              context=context)
        for backend in cmis_backend_obj.browse(cr, uid, backend_ids,
                                               context=context):
            try:
                repo = cmis_backend_obj._auth(cr, uid, backend.id,
                                              context=context)
                cmis_backend_rec = self.read(
                    cr, uid, ids, ['id_dms'], context=context)[0]
                id_dms = cmis_backend_rec['id_dms']
                # Get results from id of document
                results = repo.query(" SELECT * FROM  cmis:document WHERE \
                                     cmis:objectId ='" + id_dms + "'")
                datas = results[0].getContentStream().read().encode('base64')
                break
            except:
                continue
        return datas

    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        # We don't handle setting data to null
        if not value:
            return True
        if context is None:
            context = {}
        location = self.pool['ir.config_parameter'].get_param(
            cr, uid, 'ir_attachment.location')
        file_size = len(value.decode('base64'))
        if location:
            attach = self.browse(cr, uid, id, context=context)
            if attach.store_fname:
                self._file_delete(cr, uid, location, attach.store_fname)
            fname = self._file_write(cr, uid, location, value)
            # SUPERUSER_ID as probably don't have write access,
            # trigger during create
            super(ir_attachment, self).write(
                cr, SUPERUSER_ID, [id],
                {'store_fname': fname, 'file_size': file_size},
                context=context)
        else:
            # Don't save datas, put db_datas field to none
            super(ir_attachment, self).write(
                cr, SUPERUSER_ID, [id],
                {'db_datas': None, 'file_size': file_size}, context=context)
        return True

    def _data_get(self, cr, uid, ids, name, arg, context=None):
        """
        Get data from DMS
        """
        if context is None:
            context = {}
        result = {}
        location = self.pool['ir.config_parameter'].get_param(
            cr, uid, 'ir_attachment.location')
        bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            if location and attach.store_fname:
                result[attach.id] = self._file_read(
                    cr, uid, location, attach.store_fname, bin_size)
            elif attach.id_dms:
                datas = self.action_download(
                    cr, uid, attach.id, context=context)
                result[attach.id] = datas
                file_type, index_content = self._index(
                    cr, uid, datas.decode('base64'), attach.datas_fname, None)
                self.write(
                    cr, uid, [attach.id],
                    {'file_type': file_type, 'index_content': index_content},
                    context=context)
            else:
                raise orm.except_orm(_('Access error of document'),
                                     _("Document is not available in DMS; "
                                       "Please try again"))
        return result

    _columns = {
        'id_dms': fields.char('Id of Dms', help="Id of Dms."),
        'download_id': fields.one2many(
            'ir.attachment.download',
            'attachment_id',
            'Attachment download',
            help="Attachment download"
        ),
        'datas': fields.function(
            _data_get,
            fnct_inv=_data_set,
            string='File Content',
            type="binary",
            nodrop=True
        ),
        'attachment_document_ids': fields.one2many(
            'ir.attachment.doc.backend',
            'attachment_id',
            'Records',
            help="Records"
        ),
    }


#@job
def create_doc_in_edm(session, model_name, value, res,
                      dict_metadata, user_login, filters=None):
    """
    This method allows to create a doc from Odoo to DMS
    """
    cr = session.cr
    uid = session.uid
    context = session.context
    if context is None:
        context = {}
    ir_attach_obj = session.pool.get('ir.attachment')
    ir_attach_doc_backend_obj = session.pool.get('ir.attachment.doc.backend')
    cmis_backend_obj = session.pool.get('cmis.backend')

    # List of backend with storing_ok is True
    ids = cmis_backend_obj.search(
        cr, uid, [('storing_ok', '=', 'True')], context=context)

    for backend in session.browse('cmis.backend', ids):
        repo = cmis_backend_obj._auth(cr, uid, backend.id, context=context)
        root = repo.rootFolder
        folder_path = backend.initial_directory_write
        # Document properties
        if value.get('name'):
            file_name = value.get('name')
        elif value.get('datas_fname'):
            file_name = value.get('datas_fname')
        else:
            file_name = value.get('datas_fname')
        props = {
            'cmis:name': file_name,
            'cmis:description': value.get('description'),
            'cmis:createdBy': user_login,
        }
        # Add list of metadata in props
        if len(dict_metadata):
            for k, v in dict_metadata.iteritems():
                props[k] = v
        if folder_path:
            sub1 = repo.getObjectByPath(folder_path)
        else:
            sub1 = root
        someDoc = sub1.createDocumentFromString(
            file_name,
            contentString=base64.b64decode(
                value.get('datas')), contentType=value.get('file_type')
        )
        # TODO: create custom properties on a document (Alfresco)
        # someDoc.getProperties().update(props)
        # Updating ir.attachment object with the new id
        # of document generated by DMS
        ir_attach_obj.write(cr, uid, res, {
            'id_dms': someDoc.getObjectId()}, context=context)
        ir_attach_doc_backend_obj.create(
            cr, uid, {
                'attachment_id': res,
                'backend_id': backend.id,
                'object_doc_id': someDoc.getObjectId(),
            }, context=context)
    return True
