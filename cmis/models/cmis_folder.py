# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class CmisFolder(models.AbstractModel):
    """A model linked to a folder into cmis
    """
    _name = 'cmis.folder'
    _inherit = 'cmis.object.ref'
    _cmis_object_type = 'cmis:folder'

    @api.multi
    def _create_cmis_object(self, backend, parent_cmis_object):
        self.ensure_one()
        props = self._get_cmis_create_object_properties()
        repo = backend.check_auth()
        new_folder = repo.createFolder(
            parent_cmis_object, self.cmis_content_name, properties=props)
        return new_folder.getProperties()['cmis:objectId']
