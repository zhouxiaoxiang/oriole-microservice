# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.todo',
        'sphinx.ext.coverage',
        'sphinx.ext.viewcode',
        'sphinx.ext.intersphinx',
        ]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Service'
copyright = u'2016, Cereson'
author = u'Cereson'
version = u'V1.0'
release = u'V1.0'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'agogo'
htmlhelp_basename = 'Servicedoc'
latex_elements = {
}
latex_documents = [
    (master_doc, 'Service.tex', u'Service Documentation',
     u'Cereson', 'manual'),
]
man_pages = [
    (master_doc, 'Service', u'Service Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'Service', u'Service Documentation',
     author, 'Service', 'One line description of project.',
     'Miscellaneous'),
]


