import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-connector-cmis",
    description="Meta package for oca-connector-cmis Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-cmis',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
