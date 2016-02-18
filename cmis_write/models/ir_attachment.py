# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################
import logging
from openerp import api, fields, models
from openerp.addons.connector.session import ConnectorSession
from ..unit.import_synchronizer import create_doc_in_edm

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    id_dms = fields.Char('Id of Dms', help="Id of Dms.")
    download_id = fields.One2many(
        'ir.attachment.download',
        'attachment_id',
        'Attachment download',
        help="Attachment download"
    )

    datas = fields.Binary(
        compute='_data_get',
        inverse='_data_set')

    attachment_document_ids = fields.One2many(
        'ir.attachment.doc.backend',
        'attachment_id',
        'Records',
        help="Records"
    )

    @api.multi
    def must_be_stored_in_cmis(self):
        self.ensure_one()
        if 'bool_testdoc' in self.env.context:
            return False
        if not self.res_model:
            return False
        return True

    @api.model
    def create(self, values):
        res = super(IrAttachment, self).create(values)
        session = ConnectorSession.from_env(self.env)
        # if bool_testdoc in context, we don't need to create
        # the doc in the DMS
        # if the attachment is not linked to a model, we dont create the doc 
        # in DMSt
        if res.must_be_stored_in_cmis():
            metadata = {}
            if res.res_model:
                metadata = self.env['metadata'].extract_metadata(
                    self.env[res.res_model].browse(res.res_id))
            create_doc_in_edm.delay(
                session, 'ir.attachment', res.id, metadata,
                self.env.user.login)
        return res

    @api.multi
    def action_download(self):
        """
        Download document if it is available in one of backend
        """
        self.ensure_one()
        cmis_backend_obj = self.env['cmis.backend']
        backend = cmis_backend_obj.search([('storing_ok', '=', 'True')])
        backend.ensure_one()
        repo = backend.check_auth()
        # Get results from id of document
        query = " SELECT * FROM  cmis:document \
                WHERE cmis:objectId ='" + self.id_dms + "'"
        results = repo.query(query)
         # workaround  bug in cmislib 0.5.1
        # https://issues.apache.org/jira/browse/CMIS-701
        result = results[0]
        result.reload()
        datas = result.getContentStream().read().encode(
            'base64')
        return datas

    @api.depends('id_dms')
    @api.multi
    def _data_get(self):
        """
        Get data from DMS
        """
        for rec in self:
            if rec.id_dms:
                rec.datas = rec.action_download()
            else:
                rec.datas = super(IrAttachment, rec)._data_get(
                    'datas', None)[rec.id]

    @api.multi
    def _data_set(self):
        for rec in self:
            super(IrAttachment, rec)._data_set('datas', rec.datas, None)
