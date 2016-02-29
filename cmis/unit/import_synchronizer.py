# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp.addons.connector.unit.synchronizer import Importer
_logger = logging.getLogger(__name__)


class CmisImportSynchronizer(Importer):
    """ Base importer for Dms """

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.Environment`
        """
        super(CmisImportSynchronizer, self).__init__(environment)
        self.dms_id = None
        self.updated_on = None

    def _get_dms_data(self):
        """ Return the raw Dms data for ``self.dms_id`` in a dict
        """
        return self.backend_adapter.read(self.dms_id)

    def _map_data(self):
        """ Returns an instance of
        :py:class:`~openerp.addons.connector.unit.mapper.MapRecord`
        """
        return self.mapper.map_record(self.dms_record)

    def _get_binding_id(self):
        """Return the binding id from the dms id"""
        return self.binder.to_openerp(self.dms_id)

    def _create_data(self, map_record, **kwargs):
        return map_record.values(for_create=True, **kwargs)

    def _create(self, data):
        """ Create the OpenERP record """
        binding_id = self.session.create(self.model._name, data)

        _logger.info(
            '%s %d created from Dms %s',
            self.model._name, binding_id, self.dms_id)

        return binding_id

    def _update_data(self, map_record, **kwargs):
        return map_record.values(**kwargs)

    def _update(self, binding_id, data):
        """ Update an OpenERP record """
        self.session.write(self.model._name, binding_id, data)

        _logger.info(
            '%s %d updated from Dms record %s',
            self.model._name, binding_id, self.dms_id)

    def run(self, dms_id, options=None):
        """ Run the synchronization

        :param dms_id: identifier of the record on Dms
        :param options: dict of parameters used by the synchronizer
        """
        self.dms_id = dms_id
        self.dms_record = self._get_dms_data()

        binding_id = self._get_binding_id()

        map_record = self._map_data()
        self.updated_on = map_record.values()['updated_on']

        if binding_id:
            record = self._update_data(map_record)
            self._update(binding_id, record)
        else:
            record = self._create_data(map_record)
            binding_id = self._create(record)

        self.binder.bind(self.dms_id, binding_id)


class CmisBatchImportSynchronizer(Importer):
    def run(self, filters=None, options=None):
        raise NotImplementedError
