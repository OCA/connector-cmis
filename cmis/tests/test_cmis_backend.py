# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import mock

from psycopg2._psycopg import IntegrityError

from odoo.exceptions import AccessError
from odoo.tests import common
from odoo.tools import mute_logger


class TestCmisBackend(common.TransactionCase):
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

    def _create_internal_user(self):
        return self.env["res.users"].create(
            {
                "name": "CMIS internal user",
                "login": "cmis_internal_user",
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )

    def test_password_not_readable_by_internal_user(self):
        user = self._create_internal_user()
        backend = self.backend_instance.with_user(user)
        backend.invalidate_recordset()
        self.assertEqual(backend.name, "Test cmis")
        with self.assertRaises(AccessError):
            backend.read(["password"])
        with self.assertRaises(AccessError):
            backend.search_read([], ["password"])
        with self.assertRaises(AccessError):
            backend.read(["username"])
        with self.assertRaises(AccessError):
            backend.search_read([], ["username"])

    def test_cmis_client_internal_user(self):
        user = self._create_internal_user()
        backend = self.backend_instance.with_user(user)
        backend.invalidate_recordset()
        with mock.patch(
            "odoo.addons.cmis.models.cmis_backend.CmisClient", create=True
        ) as client, mock.patch(
            "odoo.addons.cmis.models.cmis_backend.BrowserBinding", create=True
        ):
            backend.get_cmis_client()
        args = client.call_args[0]
        self.assertEqual(args[:3], (self.vals["location"], "admin", "admin"))
