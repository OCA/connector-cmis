# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class test_metadata(TransactionCase):

    def setUp(self):
        super(test_metadata, self).setUp()
        # Clean up registries
        self.env['ir.model'].clear_caches()
        self.env['ir.model.data'].clear_caches()
        # Get registries
        self.user_model = self.env["res.users"]
        self.ir_model_model = self.env['ir.model']
        self.fields_model = self.env['ir.model.fields']
        self.metadata_model = self.env['metadata']
        # Get context
        self.ir_model = self.ir_model_model.search(
            [('model', '=', 'res.partner')])[0]

        self.field = self.fields_model.create(
            {'name': 'x_test',
             'field_description': 'test',
             'model_id': self.ir_model.id,
             'ttype': 'char',
             })

        self.vals = {
            'name': 'Test',
            'model_id': self.ir_model.id,
            'field_ids': [(4, self.field.id)],
            'metadata_list_ids': [(0, 0, {
                'field_id': self.field.id,
            })],
            'model_ids': [(4, self.ir_model.id)],
        }

    def test_create_metadata(self):
        metadata = self.metadata_model.create(self.vals)
        self.assertEqual(metadata.name, self.vals['name'])
        self.assertEqual(metadata.model_id.id, self.vals['model_id'])

    def test_onchange_model(self):
        metadata = self.metadata_model.create(self.vals)
        self.assertEqual(metadata.name, self.vals['name'])
        self.assertEqual(metadata.model_id.id, self.vals['model_id'])
        self.assertEqual(len(metadata.model_ids), 1)
        self.assertEqual(metadata.model_ids[0], self.ir_model)
