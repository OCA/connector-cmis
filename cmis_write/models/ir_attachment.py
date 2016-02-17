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

from openerp.osv import orm, fields
from openerp.addons.connector.session import ConnectorSession
from .unit.import_synchronizer import create_doc_in_edm
from openerp import SUPERUSER_ID

import logging
_logger = logging.getLogger(__name__)


class ir_attachment(orm.Model):
    _inherit = 'ir.attachment'

    def __create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        metadata_obj = self.pool['metadata']
        user_obj = self.pool['res.users']
        user_login = user_obj.browse(cr, uid, uid, context=context).login
        session = ConnectorSession(cr, uid, context=context)
        value = {}
        if values.get('datas'):
            values['index_content'] = self._index(
                cr, uid, values['datas'],
                values.get('datas_fname', False), None)
            # Get the extension file
            ext = ''
            if values.get('file_type'):
                ext = '.' + values['file_type'][values['file_type'].
                                                find('/') + 1:]
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
        if not context.get('bool_testdoc'):
            # Don't save the document in Odoo/OpenERP
            values['datas'] = None
        # Create an ir.attachment
        res = super(ir_attachment, self).create(
            cr, uid, values, context=context)
        # if bool_testdoc in context, we don't need to create
        # the doc in the DMS
        if not context.get('bool_testdoc'):
                create_doc_in_edm.delay(
                    session, 'ir.attachment', value, res, dict_metadata,
                    user_login)
        return res

    def action_download(self, cr, uid, ids, context=None):
        """
        Download document if it is available in one of backend
        """
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        cmis_backend_obj = self.pool['cmis.backend']
        datas = ''
        for ir in self.browse(cr, uid, ids, context=context):
            # Get the created document from cmis_write.
            # Document is stored from DMS.
            if len(ir.attachment_document_ids) != 0:
                for doc in ir.attachment_document_ids:
                    try:
                        backend = cmis_backend_obj.search(
                            cr, uid, [
                                ('id', '=', doc.backend_id.id),
                                ('storing_ok', '=', 'True')
                            ], context=context)
                        # Connect to the backend
                        repo = cmis_backend_obj.check_auth(
                            cr, uid, backend, context=context)
                        # Get the id of document
                        id_dms = doc.object_doc_id
                        # Get results from id of document
                        query = " SELECT * FROM  cmis:document \
                                WHERE cmis:objectId ='" + id_dms + "'"
                        results = repo.query(query)
                        datas = results[0].getContentStream().read().encode(
                            'base64')
                        return datas
                    except:
                        continue
            else:
                # Get the created document from cmis_read.
                # Document is directly stored in Odoo/OpenERP.
                return ir.db_datas
        return datas

    def __data_set(self, cr, uid, id, name, value, arg, context=None):
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
            # Don't save data if the document comes from DMS
            if not context.get('bool_testdoc'):
                value = None
            super(ir_attachment, self).write(
                cr, SUPERUSER_ID, [id],
                {'db_datas': value, 'file_size': file_size}, context=context)
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
            datas = self.action_download(cr, uid, attach.id, context=context)
            if location and attach.store_fname:
                result[attach.id] = self._file_read(
                    cr, uid, location, attach.store_fname, bin_size)
            elif len(attach.attachment_document_ids) == 0:
                result[attach.id] = datas
            else:
                if attach.id_dms:
                    if datas:
                        result[attach.id] = datas
                    else:
                        result[attach.id] = ''
                        _logger.warn('Access error of DMS')
                else:
                    result[attach.id] = ''
                    _logger.warn('Attachment %s has no id_dms', attach.name)
        return result

    _columns = {
        'id_dms': fields.char('Id of Dms', help="Id of Dms."),
        'download_id': fields.one2many(
            'ir.attachment.download',
            'attachment_id',
            'Attachment download',
            help="Attachment download"
        ),
        #'datas': fields.function(
        #    _data_get,
        #    fnct_inv=_data_set,
        #    string='File Content',
        #    type="binary",
        #    nodrop=True
        #),
        'attachment_document_ids': fields.one2many(
            'ir.attachment.doc.backend',
            'attachment_id',
            'Records',
            help="Records"
        ),
    }
