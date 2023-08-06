# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_pagination_bootstrap', 'django_pagination_bootstrap.templatetags']

package_data = \
{'': ['*'], 'django_pagination_bootstrap': ['templates/*']}

install_requires = \
['django>=2.0']

setup_kwargs = {
    'name': 'django-pagination-bootstrap',
    'version': '2.4.4',
    'description': "Easy add pagination in Django, using Bootstrap's layout.",
    'long_description': 'Django Pagination Bootstrap\n===========================\n\n**MAINTAINER NEEDED: this project is complete but won\'t be updated until further notice. If you have interest in improving it, please contact me by creating an** `issue here`_ **.**\n\n.. badges-begin\n\n|PyPI| |Python Version| |License|\n\n|Tests| |Codecov|\n\n|Black| |pre-commit|\n\n.. |PyPi| image:: https://badge.fury.io/py/django-pagination-bootstrap.svg\n   :target: https://badge.fury.io/py/django-pagination-bootstrap\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/django-pagination-bootstrap\n   :target: https://pypi.org/project/django-pagination-bootstrap\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/django-pagination-bootstrap\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Tests| image:: https://github.com/staticdev/django-pagination-bootstrap/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/django-pagination-bootstrap/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/django-pagination-bootstrap/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/staticdev/django-pagination-bootstrap\n   :alt: Codecov\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n\nDjango-pagination-bootstrap is an app to easy add pagination in Django_, using `Bootstrap`_\'s layout.\n\nNote: This library currently works with Python 3.6+, Django 2.0+ and Bootstrap 3+. For older versions, please use version 1.3.0.\n\nInstallation\n------------\n\nTo install ``django-pagination-bootstrap`` simply run:\n\n.. code:: console\n\n   pip install django-pagination-bootstrap\n\nConfiguration\n-------------\n\nWe need to hook ``django-pagination-bootstrap`` into our project.\n\n1. Put ``django-pagination-bootstrap`` into your ``INSTALLED_APPS`` at settings module:\n\n.. code-block:: python\n\n   INSTALLED_APPS = (\n       # other apps\n       "django_pagination_bootstrap",\n   )\n\n2. Install the pagination middleware. Your settings file might look something like:\n\n.. code-block:: python\n\n   MIDDLEWARE_CLASSES = (\n       # other middleware\n       "django_pagination_bootstrap.middleware.PaginationMiddleware",\n   )\n\n3. Guarantee you have ``django.template.context_processors.request`` on settings.py:\n\n.. code-block:: python\n\n   TEMPLATES = [\n       {\n           # ...\n           "OPTIONS": {\n               "context_processors": [\n                   # ...\n                   "django.template.context_processors.request"\n                   # ...\n               ],\n           },\n       },\n   ]\n\n4. Add this line at the top of your template to load the pagination tags:\n\n.. code-block:: python\n\n   {% load pagination_tags %}\n\n5. Decide on a variable that you would like to paginate, and use the autopaginate tag on that variable before iterating over it. This could take one of two forms (using the canonical object_list as an example variable):\n\n.. code-block:: python\n\n   {% autopaginate object_list %}\n\n\nThis assumes that you would like to have the default 20 results per page. If you would like to specify your own amount of results per page, you can specify that like so:\n\n.. code-block:: python\n\n   {% autopaginate object_list 10 %}\n\nNote that this replaces object_list with the list for the current page, so you can iterate over the object_list like you normally would.\n\n6. Now you want to display the current page and the available pages, so somewhere after having used autopaginate. If you are using Bootstrap 3, use the paginate inclusion tag:\n\n.. code-block:: python\n\n   {% paginate %}\n\nThis does not take any arguments, but does assume that you have already called autopaginate, so make sure to do so first.\n\nThat\'s it! You have now paginated object_list and given users of the site a way to navigate between the different pages--all without touching your views.\n\nSide effects\n------------\n\nA django-paginator_ instance will be injected in the template context as ``paginator``. You can access it as usual:\n\n.. code-block:: python\n\n   page {{ page }} of {{ paginator.num_pages }}\n\nOptional Settings\n-----------------\n\nIn django-pagination, there are no required settings. There are, however, a small set of optional settings useful for changing the default behavior of the pagination tags. Here\'s an overview:\n\n* PAGINATION_DEFAULT_PAGINATION\n\nThe default amount of items to show on a page if no number is specified.\n\n* PAGINATION_DEFAULT_WINDOW\n\nThe number of items to the left and to the right of the current page to display (accounting for ellipses).\n\n* PAGINATION_DEFAULT_ORPHANS\n\nThe number of orphans allowed. According to the Django documentation, orphans are defined as:\n\n   The minimum number of items allowed on the last page, defaults to zero.\n\n* PAGINATION_INVALID_PAGE_RAISES_404\n\nDetermines whether an invalid page raises an Http404 or just sets the invalid_page context variable.  True does the former and False does the latter.\n\nCredits\n-------\n\nThis is based on Eric Florenzano\'s django-pagination 1.0.7 and is an updated version of https://github.com/tgdn/django-bootstrap-pagination for Django 1.7 or higher.\n\n.. _issue here: https://github.com/staticdev/staticdev/issues\n.. _Django: https://www.djangoproject.com/\n.. _Bootstrap: http://getbootstrap.com/\n.. _django-pagination: https://pypi.python.org/pypi/django-pagination\n.. _django-paginator: https://docs.djangoproject.com/en/dev/topics/pagination/#paginator-objects\n',
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/django-pagination-bootstrap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
