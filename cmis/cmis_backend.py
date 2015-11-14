# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp.addons.connector.connector import Environment
from openerp.addons.connector.session import ConnectorSession
from .unit.backend_adapter import CmisAdapter
import cmislib.exceptions


class cmis_backend(orm.Model):
    _name = 'cmis.backend'
    _description = 'CMIS Backend'
    _inherit = 'connector.backend'
    _backend_type = 'cmis'
    _columns = {
        'version': fields.selection(
            lambda self, *a, **kw: self._select_versions(*a, **kw),
            'Version',
            required=True,
        ),
        'location': fields.char(
            'Location',
            required=True,
        ),
        'username': fields.char(
            'Username',
            required=True,
        ),
        'password': fields.char(
            'Password',
            required=True,
        ),
        'initial_directory_read': fields.char(
            'Initial directory for reading',
            required=True,
        ),
        'initial_directory_write': fields.char(
            'Initial directory for writing',
            required=True,
        ),
        'browsing_ok': fields.boolean(
            'Allow browsing this backend',
        ),
        'storing_ok': fields.boolean(
            'Allow storing in this backend',
        ),
    }
    _defaults = {
        'initial_directory_read': '/',
        'initial_directory_write': '/',
    }

    def select_versions(self, cr, uid, context=None):
        """ Available versions in the backend.
        Can be inherited to add custom versions. Using this method
        to add a version from an ``_inherit`` does not constrain
        to redefine the ``version`` field in the ``_inherit`` model.
        """
        return [('1.0', '1.0')]

    def _select_versions(self, cr, uid, context=None):
        """ Available versions in the backend.
        If you want to add a version, do not override this
        method, but ``select_version``.
        """
        return self.select_versions(cr, uid, context=context)

    def _get_base_adapter(self, cr, uid, ids, context=None):
        """
        Get an adapter to test the backend connection
        """
        backend = self.browse(cr, uid, ids[0], context=context)
        session = ConnectorSession(cr, uid, context=context)
        environment = Environment(backend, session, None)

        return CmisAdapter(environment)

    def check_auth(self, cr, uid, ids, context=None):
        """ Check the authentication with DMS """

        adapter = self._get_base_adapter(cr, uid, ids, context=context)
        return adapter._auth(ids)

    def check_directory_of_write(self, cr, uid, ids, context=None):
        """Check access right to write from the path"""
        if context is None:
            context = self.pool['res.users'].context_get(cr, uid)
        cmis_backend_obj = self.pool.get('cmis.backend')
        datas_fname = 'testdoc'
        # login with the cmis account
        repo = self.check_auth(cr, uid, ids, context=context)
        cmis_backend_rec = cmis_backend_obj.read(
            cr, uid, ids, ['initial_directory_write'],
            context=context)[0]
        folder_path_write = cmis_backend_rec['initial_directory_write']
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
                raise orm.except_orm(
                    _('Cmis  Error!'),
                    _("The test file already exists in the DMS. "
                      "Please remove it and try again."))
            except cmislib.exceptions.RuntimeException:
                raise orm.except_orm(
                    _('Cmis access right Error!'),
                    ("Please check your access right."))
        self.get_error_for_path(bool_path_write, folder_path_write)

    def check_directory_of_read(self, cr, uid, ids, context=None):
        """Check access right to read from the path"""
        if context is None:
            context = self.pool['res.users'].context_get(cr, uid)
        cmis_backend_rec = self.read(
            cr, uid, ids, ['initial_directory_read'],
            context=context)[0]
        # Login with the cmis account
        repo = self.check_auth(cr, uid, ids, context=context)
        folder_path_read = cmis_backend_rec['initial_directory_read']
        # Testing the path
        rs = repo.query("SELECT cmis:path FROM  cmis:folder ")
        bool_path_read = self.check_existing_path(rs, folder_path_read)
        self.get_error_for_path(bool_path_read, folder_path_read)

    def check_existing_path(self, rs, folder_path):
        """Function to check if the path is correct"""
        for one_rs in rs:
            # Print name of files
            props = one_rs.getProperties()
            if props['cmis:path'] == folder_path:
                return True
        return False

    def get_error_for_path(self, is_valid, path):
        """Return following the boolean the right error message"""
        if is_valid:
            raise orm.except_orm(_('Cmis  Message'),
                                 _("Path is correct for : %s") % path)
        else:
            raise orm.except_orm(_('Cmis  Error!'),
                                 _("Error path for : %s") % path)

    def sanitize_input(self, file_name):
        """Prevent injection by escaping: '%_"""
        file_name = file_name.replace("'", r"\'")
        file_name = file_name.replace("%", r"\%")
        file_name = file_name.replace("_", r"\_")
        return file_name

    def safe_query(self, query, file_name, repo):
        args = map(self.sanitize_input, file_name)
        return repo.query(query % ''.join(args))
