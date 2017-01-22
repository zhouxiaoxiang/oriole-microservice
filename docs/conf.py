import os
import sys
import pkg_resources

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
project = 'Oriole-service'
copyright = '2017, Eric.Zhou'
author = u'Eric.Zhou'
version = pkg_resources.get_distribution('oriole-service').version
release = version
exclude_patterns = []
pygments_style = 'sphinx'
modindex_common_prefix = ['oriole-service.']
html_theme = 'agogo'
htmlhelp_basename = 'Oriole-Servicedoc'
latex_elements = {
}
latex_documents = [
    (master_doc, 'Oriole-Service.tex', u'Oriole-Service Documentation',
     'Eric.Zhou', 'manual'),
]
man_pages = [
    (master_doc, 'Oriole-Service', 'Oriole-Service Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'Oriole-Service', u'Oriole-Service Documentation',
     author, 'Eric.Zhou', 'One line description of project.',
     'Miscellaneous'),
]
