# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###############################################################################

from openerp.tests.common import TransactionCase


class test_ir_attachment(TransactionCase):

    def setUp(self):
        super(test_ir_attachment, self).setUp()
        # Clean up registries
        self.env['ir.model'].clear_caches()
        self.env['ir.model.data'].clear_caches()
        # Get registries
        self.user_model = self.env["res.users"]
        self.ir_attachment_model = self.env["ir.attachment"]
        self.partner_model = self.env['res.partner']
        self.metadata_model = self.env['metadata']
        partner_id = self.partner_model.create(
            {'name': 'Test Partner',
             'email': 'test@localhost',
             'is_company': True,
             })

        blob1 = 'blob1'
        blob1_b64 = blob1.encode('base64')

        self.vals = {
            'name': 'a1',
            'datas': blob1_b64,
            'attachment_document_ids': [(0, 0, {
                'res_model': "res.partner",
                'res_id': partner_id,
                'res_name': 'Test Partner',
            })],
        }

    def test_create_ir_attachment(self):
        vals = self.vals
        vals['datas'] = None
        ir_attachment = self.ir_attachment_model.with_context(
            bool_testdoc=True).create(vals)
        self.assertEqual(ir_attachment.name, vals['name'])

    def test_data_get_set(self):
        ir_attachment = self.ir_attachment_model.with_context(
            bool_testdoc=True).create(self.vals)
        self.assertTrue(ir_attachment.datas)
