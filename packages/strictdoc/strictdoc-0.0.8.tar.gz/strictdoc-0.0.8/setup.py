# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strictdoc',
 'strictdoc.backend',
 'strictdoc.backend.dsl',
 'strictdoc.backend.dsl.models',
 'strictdoc.cli',
 'strictdoc.core',
 'strictdoc.core.actions',
 'strictdoc.export.excel',
 'strictdoc.export.html',
 'strictdoc.export.html.generators',
 'strictdoc.export.html.renderers',
 'strictdoc.export.html.tools',
 'strictdoc.export.rst',
 'strictdoc.helpers']

package_data = \
{'': ['*'],
 'strictdoc.export.html': ['_static/*',
                           'templates/*',
                           'templates/_shared/*',
                           'templates/document_tree/*',
                           'templates/single_document/*',
                           'templates/single_document_table/*',
                           'templates/single_document_traceability/*',
                           'templates/single_document_traceability_deep/*']}

install_requires = \
['XlsxWriter>=1.3.7,<2.0.0',
 'docutils==0.16',
 'jinja2==2.11.2',
 'python-datauri>=0.2.9,<0.3.0',
 'textx==2.3.0']

entry_points = \
{'console_scripts': ['strictdoc = strictdoc.cli.main:main']}

setup_kwargs = {
    'name': 'strictdoc',
    'version': '0.0.8',
    'description': ' Software for writing technical requirements and specifications.',
    'long_description': '# StrictDoc\n\n![](https://github.com/stanislaw/strictdoc/workflows/StrictDoc%20on%20macOS/badge.svg)\n![](https://github.com/stanislaw/strictdoc/workflows/StrictDoc%20on%20Linux/badge.svg)\n![](https://github.com/stanislaw/strictdoc/workflows/StrictDoc%20on%20Windows/badge.svg)\n\nThe project and the repository are under construction.\n\nThe documentation is hosted on Read the Docs:\n[StrictDoc documentation](https://strictdoc.readthedocs.io/en/latest/).\n',
    'author': 'Stanislav Pankevich',
    'author_email': 's.pankevich@gmail.com',
    'maintainer': 'Stanislav Pankevich',
    'maintainer_email': 's.pankevich@gmail.com',
    'url': 'https://github.com/stanislaw/strictdoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
