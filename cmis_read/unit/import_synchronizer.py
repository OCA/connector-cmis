# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 - Present Savoir-faire Linux
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.addons.connector.queue.job import job


@job
def create_doc_from_dms(session, model_name, data, name, model, res_id,
                        uid, filters=None):
    cr = session.cr
    uid = session.uid
    context = session.context
    if context is None:
        context = {}
    cmis_backend_obj = session.pool.get('cmis.backend')
    ids = cmis_backend_obj.search(
        cr, uid, [('browsing_ok', '=', 'True')], context=context)
    for backend in session.browse('cmis.backend', ids):
        try:
            repo = cmis_backend_obj.check_auth(
                cr, uid, [backend.id], context=context)
            for attach in session.browse(
                    'ir.attachment.dms', data['attachment_ids']):
                # Get results from id of document
                results = repo.query(" SELECT * FROM  cmis:document WHERE \
                                     cmis:objectId ='" + attach.file_id + "'")
                for result in results:
                    info = result.getProperties()
                    data_attach = {
                        'name': info['cmis:name'],
                        'description': info['cmis:description'],
                        'type': 'binary',
                        'datas':
                        result.getContentStream().read().encode('base64'),
                        'res_model': model,
                        'res_name': name,
                        'res_id': res_id,
                        'user_id': uid,
                        'datas_fname': info['cmis:name'],
                    }
                    # Store the document in Odoo/OpenERP, no need to search
                    # in the DMS after creation
                    with session.change_context({'bool_testdoc': True}):
                        session.create('ir.attachment', data_attach)
            break
        except:
            continue
    return True
