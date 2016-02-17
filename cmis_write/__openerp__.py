# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CMIS Write',
    'version': '9.0.1.0.0',
    'category': 'Knowledge Management',
    'summary': 'Create Document in DMS from Odoo/OpenERP',
    'description': """
Add Documents from Odoo/OpenERP
===============================

This module allows you to store Odoo/OpenERP document in the DMS repository.

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
============

To manage a custom aspect using CMIS (and all the other supported ways)
you have to:

* Define a new custom model configuring Alfresco. To do this I suggest you
http://wiki.alfresco.com/wiki/Step-By-Step:_Creating_A_Custom_Model.

* Add the custom aspect to the document you upload or create in Alfresco.
Using CMIS I suggest you:
http://docs.alfresco.com/4.1/index.jsp?topic=%2Fcom.alfresco.enterprise.doc%2Fconcepts%2Fopencmis-ext-adding.html.

* Set the custom property in the way you probably know using CMIS.

Contributors
------------
* El Hadji Dem (elhadji.dem@savoirfairelinux.com)
""",
    'author': 'Savoir-faire Linux',
    'website': 'www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'depends': [
        'document',
        'cmis',
    ],
    'data': [
        'views/document_view.xml',
        'views/metadata_view.xml',
        'security/ir.model.access.csv',
    ],
    'js': [
        'static/src/js/document.js'
    ],
    'qweb': [],
    'test': [],
    'demo': [],
    'installable': False,
    'auto_install': False,
}
