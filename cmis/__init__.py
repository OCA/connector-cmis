# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import functools
import logging
from . import models

_logger = logging.getLogger(__name__)
try:
    import httplib2
except (ImportError, IOError) as err:
    _logger.debug(err)


httplib2.Http = functools.partial(
    httplib2.Http, disable_ssl_certificate_validation=True
)
