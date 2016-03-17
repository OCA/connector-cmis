# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.exceptions import UserError
from openerp.tools.translate import _


class CmisObjectRef(models.AbstractModel):
    """A technical model to hold a reference to an object into
    a cmis container
    """
    _name = 'cmis.object.ref'
    _cmis_object_type = None  # The object type in cmis ex :cmis:folder

    cmis_objectid = fields.Char(
        string="CMIS ObjectId", requried=True, index=True, copy=False)
    backend_id = fields.Many2one(
        comodel_name="cmis.backend",
        string="Backend",
        copy=False) 
    
    cmis_content_name = fields.Char(compute='get_names_for_cmis_content')
    
    _sql_constraints = [
            ('cmis_object_ref_uniq',
             'unique (objectid, backend_id)',
             "Cmis object Id must be uniquein a given backend !"),
    ]

    @api.multi
    def get_names_for_cmis_content(self):
        names = dict(self.name_get())
        for rec in self:
            rec.cmis_content_name = names[rec.id]

    @api.model
    def get_initial_directory_write(self, backend):
        return '/'.join([backend.initial_directory_write,
                         self._name.replace('.', '_')])

    @api.multi
    def _get_cmis_create_object_properties(self):
        """Return a dictionary of cmis properties to apply when
        creating the cmis object
        """
        self.ensure_one()
        ret = {}
        if self._cmis_object_type:
            ret['cmis:objectTypeId'] = self._cmis_object_type
        return ret

    def _create_cmis_object(self, backend, parent_cmis_object):
        raise NotImplementedError('Must be implemented by specific types')

    @api.multi
    def create_in_cmis(self, backend_id):
        backend = self.env['cmis.backend'].browse(backend_id)
        backend.ensure_one()
        vals = {}
        for rec in self:
            if rec.cmis_objectid:
                raise UserError(
                    _("Object %s already exists in CMIS (backend: %s)" % (
                      rec.name, rec.backend_id.name)))
            parent_cmis_object = backend.get_folder_by_path(
                self.get_initial_directory_write(backend),
                create_if_not_found=True)
            cmis_objectid = rec._create_cmis_object(
                backend, parent_cmis_object)
            rec.write({
                'cmis_objectid': cmis_objectid,
                'backend_id': backend.id
                })
            vals[rec.id] = cmis_objectid
        return vals
