# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.exceptions import Warning
from openerp.tools.translate import _


class CmisFolder(models.AbstractModel):
    """A model linked to a folder into cmis
    """
    _name = 'cmis.folder'
    _inherit = 'cmis.object.ref'

    name = fields.Char()

    @api.model
    def get_initial_directory_write(self, backend):
        return '/'.join([backend.initial_directory_write, 
                         self._name.replace('.', '_')])

    @api.multi
    def _create_cmis_content(self, backend, parent_cmis_object):
        self.ensure_one()
        repo = backend.check_auth()
        new_folder = repo.createFolder(parent_cmis_object, self.name)
        return new_folder.getProperties()['cmis:objectId']

    @api.multi
    def create_in_cmis(self, backend_id):
        backend = self.env['cmis.backend'].browse(backend_id)
        backend.ensure_one()
        vals ={}
        for rec in self:
            if rec.cmis_objectid:
                raise Warning(
                    _("Folder %s already exists in CMIS (backend: %s)" % (
                      rec.name, rec.backend_id.name)))
            parent_cmis_object = backend.get_folder_by_path(
                self.get_initial_directory_write(backend),
                create_if_not_found=True)
            cmis_objectid = rec._create_cmis_content(
                backend, parent_cmis_object)
            rec.write({
                'cmis_objectid': cmis_objectid,
                'backend_id': backend.id
                })
            vals[rec.id] = cmis_objectid
        return vals
