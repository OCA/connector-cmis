# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models
from openerp.tools.translate import _


class CmisObjectRef(models.AbstractModel):
    """A technical model to hold a reference to an object into
    a cmis container
    """
    _name = 'cmis.object.ref'

    cmis_objectid = fields.Char(
        string="CMIS ObjectId", requried=True, index=True)
    backend_id = fields.Many2one(
        comodel_name="cmis.backend",
        string="Backend") 

    _sql_constraints = [
            ('cmis_object_ref_uniq',
             'unique (objectid, backend_id)',
             "Cmis object Id must be uniquein a given backend !"),
    ]
