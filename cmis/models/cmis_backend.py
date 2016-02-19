# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import cmislib.exceptions
from cmislib.exceptions import ObjectNotFoundException

from openerp import api, fields, models
from openerp.exceptions import Warning
from openerp.tools.translate import _
from openerp.addons.connector.connector import ConnectorEnvironment
from openerp.addons.connector.session import ConnectorSession
from ..unit.backend_adapter import CmisAdapter
from ..exceptions import CMISError


class CmisBackend(models.Model):
    _name = 'cmis.backend'
    _description = 'CMIS Backend'
    _inherit = 'connector.backend'

    _backend_type = 'cmis'

    version = fields.Selection(
        selection=[('1.0', '1.0')], required=True)
    location = fields.Char(
        required=True)
    username = fields.Char(
        required=True)
    password = fields.Char(
        required=True)
    initial_directory_read = fields.Char(
        'Initial directory for reading', required=True, default='/')
    initial_directory_write = fields.Char(
        'Initial directory for writing', required=True, default='/')
    browsing_ok = fields.Boolean(
        'Allow browsing this backend')
    storing_ok = fields.Boolean(
        'Allow storing in this backend')

    @api.multi
    def _get_base_adapter(self):
        """
        Get an adapter to test the backend connection
        """
        self.ensure_one()
        session = ConnectorSession.from_env(self.env)
        environment = ConnectorEnvironment(self, session, None)
        return CmisAdapter(environment)

    @api.multi
    def check_auth(self):
        """ Check the authentication with DMS """
        self.ensure_one()
        adapter = self._get_base_adapter()
        return adapter._auth(self)

    @api.multi
    def check_directory_of_write(self):
        """Check access right to write from the path"""
        datas_fname = 'testdoc'
        for this in self:
            # login with the cmis account
            repo = this.check_auth()
            folder_path_write = this.initial_directory_write
            # Testing the path
            rs = repo.query("SELECT cmis:path FROM  cmis:folder")
            bool_path_write = self.check_existing_path(rs, folder_path_write)
            # Check if we can create a doc from OE to EDM
            # Document properties
            if bool_path_write:
                sub = repo.getObjectByPath(folder_path_write)
                try:
                    sub.createDocumentFromString(
                        datas_fname,
                        contentString='hello, world',
                        contentType='text/plain')
                except cmislib.exceptions.UpdateConflictException:
                    raise CMISError(
                        _("The test file already exists in the DMS. "
                          "Please remove it and try again."))
                except cmislib.exceptions.RuntimeException:
                    raise CMISError(
                        ("Please check your access right."))
            self.get_error_for_path(bool_path_write, folder_path_write)

    @api.multi
    def check_directory_of_read(self):
        """Check access right to read from the path"""
        for this in self:
            repo = this.check_auth()
            folder_path_read = this.initial_directory_read
            # Testing the path
            rs = repo.query("SELECT cmis:path FROM  cmis:folder ")
            bool_path_read = self.check_existing_path(rs, folder_path_read)
            self.get_error_for_path(bool_path_read, folder_path_read)

    @api.multi
    def get_object_by_path(self, path, create_if_not_found=True):
        self.ensure_one()
        repo = self.check_auth()
        traversed = []
        for part in path.split('/'):
            try:
                part = '%s' % part
                traversed.append(part)
                new_root = repo.getObjectByPath('/'.join(traversed))
            except ObjectNotFoundException:
                if create_if_not_found:
                    new_root = repo.createFolder(root, part)
                else:
                    return False
            root = new_root
        return root

    def check_existing_path(self, rs, folder_path):
        """Function to check if the path is correct"""
        for one_rs in rs:
            # Print name of files
            cmis_path = one_rs.getProperties()['cmis:path']
            if folder_path == cmis_path or folder_path in cmis_path:
                return True
        return False

    def get_error_for_path(self, is_valid, path):
        """Return following the boolean the right error message"""
        if is_valid:
            raise Warning(_("Path is correct for : %s") % path)
        else:
            raise CMISError(_("Error path for : %s") % path)

    def sanitize_input(self, file_name):
        """Prevent injection by escaping: '%_"""
        file_name = file_name.replace("'", r"\'")
        file_name = file_name.replace("%", r"\%")
        file_name = file_name.replace("_", r"\_")
        return file_name

    def safe_query(self, query, file_name, repo):
        args = map(self.sanitize_input, file_name)
        return repo.query(query % ''.join(args))
