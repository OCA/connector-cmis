# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2._psycopg import IntegrityError

from odoo.exceptions import AccessError
from odoo.tests import common
from odoo.tools import mute_logger


class TestCmisBackend(common.SavepointCase):
    def setUp(self):
        super(TestCmisBackend, self).setUp()
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

    def test_internal_user_no_access(self):
        user = self.env["res.users"].create(
            {
                "name": "CMIS internal user",
                "login": "cmis_internal_user",
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )
        backend = self.backend_instance.with_user(user)
        with self.assertRaises(AccessError):
            self.cmis_backend.with_user(user).search_read([], ["password"])
        with self.assertRaises(AccessError):
            backend.read(["username", "password"])
        with self.assertRaises(AccessError):
            backend.get_folder_by_path("/")
