# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "CMIS",
    "version": "14.0.1.0.1",
    "development_status": "Mature",
    "category": "Connector",
    "summary": "Connect Odoo with a CMIS server",
    "author": "Savoir-faire Linux, "
    "ACSONE SA/NV, "
    "Odoo Community Association (OCA)",
    "maintainers": ["lmignon"],
    "website": "https://github.com/OCA/connector-cmis",
    "license": "AGPL-3",
    "external_dependencies": {"python": ["cmislib"]},
    "data": ["security/cmis_backend.xml", "views/cmis_backend.xml"],
    "demo": ["demo/cmis_backend_demo.xml"],
    "installable": True,
}
