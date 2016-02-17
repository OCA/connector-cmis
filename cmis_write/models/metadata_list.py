# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class MetadataList(models.Model):
    _description = 'List of Metadata'
    _name = 'metadata.list'

    field_id = fields.Many2one(
        'ir.model.fields',
        'Fields',
        help="Fields"
    )
    metadata_id = fields.Many2one(
        'metadata',
        'Metadata',
        help="Metadata"
    )
