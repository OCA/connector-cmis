# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class Metadata(models.Model):
    _name = "metadata"
    _description = "Metadata"
    name = fields.Char("Name", required=True, select=1, help="Name")
    model_id = fields.Many2one(
        'ir.model',
        'Model',
        required=True,
        select=1,
    )
    field_ids = fields.Many2many(
        'ir.model.fields',
        'metadata_field_rel',
        'meta_id', 'field_id',
        'Fields',
    )
    metadata_list_ids = fields.One2many(
        'metadata.list',
        'metadata_id',
        'List of fields',
        help="List of fields"
    )
    model_ids = fields.Many2many(
        'ir.model',
        string='Model List',
        help="Model List"
    )

    @api.model
    def extract_metadata(self, instance):
        """Extract metadata for the given model instance
        """
        metadata = {}
        if not instance:
            return metadata
        # Get list of metadata
        fields = self.env['metadata.list'].search([
            ('metadata_id.model_id.model', '=', instance._name)])
        list_fields = fields.mapped('field_id.name')
        for attr in list_fields:
            metadata['cmis:' + attr] = getattr(instance, attr)
        return metadata

    @api.onchange('model_id')
    def onchange_model(self):
        if not self.model_id:
            self.model_ids = [(6, 0, [])]
        model_ids = [self.model_id.id]
        if self.model_id._inherits:
            for key in self.model_id._inherits.keys():
                found_model_ids = self.model_id.search(
                    [('model', '=', key)])
                model_ids += found_model_ids._ids
        self.model_ids = [(6, 0, model_ids)]
