# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2._psycopg import IntegrityError

from odoo.tests import common
from odoo.tools import mute_logger


class TestCmisBackend(common.SavepointCase):
    def setUp(self):
        super().setUp()
        self.vals = {
            "name": "Test cmis",
            "location": "http://localhost:8081/alfresco/s/cmis",
            "username": "admin",
            "password": "admin",
            "initial_directory_write": "/",
        }
        self.cmis_backend = self.env["cmis.backend"]
        self.backend_instance = self.cmis_backend.create(self.vals)

    @mute_logger("odoo.sql_db")
    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            self.cmis_backend.create(self.vals)

    def test_requests_timeout(self):
        # test default ir_config_parameter
        timeout = self.cmis_backend.get_requests_timeout()
        self.assertEqual(timeout, 10)

        # test ir_config_parameter different from fallback in method
        self.env["ir.config_parameter"].sudo().set_param(
            "cmis.requests_timeout", 13)
        timeout = self.cmis_backend.get_requests_timeout()
        self.assertEqual(timeout, 13)

        # test default from method if faulty value in ir_config_parameter
        self.env["ir.config_parameter"].sudo().set_param(
            "cmis.requests_timeout", "faulty")
        timeout = self.env["ir.config_parameter"].sudo().get_param(
            "cmis.requests_timeout")
        self.assertEqual(timeout, "faulty")
        timeout = self.cmis_backend.get_requests_timeout()
        self.assertEqual(timeout, 10)

        # test default from method if missing ir_config_parameter
        param = self.env["ir.config_parameter"].sudo().search([
            ('key', '=', "cmis.requests_timeout")])
        param.unlink()
        timeout = self.env["ir.config_parameter"].sudo().get_param(
            "cmis.requests_timeout", "missing")
        self.assertEqual(timeout, "missing")
        timeout = self.cmis_backend.get_requests_timeout()
        self.assertEqual(timeout, 10)
