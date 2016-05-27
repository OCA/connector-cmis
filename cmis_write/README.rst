.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Add Documents from Odoo/OpenERP
===============================

This module allows you to store Odoo/OpenERP document in the DMS repository.

Installation
============

No installation required:

Configuration
=============

* Create a new CMIS backend with the host, login and password.
* Configure the path in the repository where documents will be dropped.
  By default, it uses the home directory of the user.

Usage
=====

* On one Odoo/OpenERP record, click "Add document".
* Upload your documents
* Uploaded documents will be enqueued for storage in the DMS
  (Document Management System)

Add Metadata
------------

To manage a custom aspect using CMIS (and all the other supported ways)
you have to:

* Define a new custom model configuring Alfresco. To do this I suggest you
http://wiki.alfresco.com/wiki/Step-By-Step:_Creating_A_Custom_Model.

* Add the custom aspect to the document you upload or create in Alfresco.
Using CMIS I suggest you:
http://docs.alfresco.com/4.1/index.jsp?topic=%2Fcom.alfresco.enterprise.doc%2Fconcepts%2Fopencmis-ext-adding.html.

* Set the custom property in the way you probably know using CMIS.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/104/9.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/connector-cmis/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/connector-cmis/issues/new?body=module:%20cmis_write%0Aversion:%20
9.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* El Hadji Dem <elhadji.dem@savoirfairelinux.com>
* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>
* Laurent Mignon <laurent.mignon@acsone.eu>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
