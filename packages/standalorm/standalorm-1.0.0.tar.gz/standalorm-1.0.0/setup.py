# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['standalorm']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.5,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'dj-database-url>=0.5.0,<0.6.0',
 'path>=15.0.1,<16.0.0',
 'pathvalidate>=2.3.2,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['standalorm = standalorm.cli:cli']}

setup_kwargs = {
    'name': 'standalorm',
    'version': '1.0.0',
    'description': "A Python library that enables you to harness the power of Django's ORM in standalone Python scripts.",
    'long_description': '# standalorm\n\nA Python library that enables you to harness the power of Django\'s ORM in standalone\nPython scripts.\n\n## Installation\n\n```\n$ pip install standalorm\n```\n\n## Usage\n\nGetting started with standalorm is quick and easy.\n\n1. Create a Django app in your project\'s root directory:\n\n    ```\n    $ standalorm startapp\n    ```\n\n2. Create your models in `app-directory/models.py`:\n\n    ```python\n    from django.db import models\n    \n    # For demonstration purposes only.\n    class ExampleModel(models.Model):\n        exampleField = models.Field()\n    ```\n\n3. Make and apply your migrations:\n\n    ```\n    $ standalorm makemigrations\n    ```\n    ```\n    $ standalorm migrate\n    ```\n \n4. Import the `orm_init()` function into your code and call it with the dunder variable `__file__` as its sole argument:\n\n    ```python\n    from standalorm import orm_init\n    \n    orm_init(__file__)\n    ```\n\n5. Finally, import your models:\n\n    ```python\n    # orm_init() must be imported AND called before this!\n    \n    from db import models  # Replace "db" with the name of your Django app if necessary\n    \n    # Do stuff with your models here\n    ```\n\nThat\'s it.\n\nThis example doesn\'t demonstrate the full extent of standalorm\'s capabilities. \nYou\'ll have to see the [documentation](https://standalorm.readthedocs.io) for that.\n\n## Database Support\n\nstandalorm supports Oracle, PostgreSQL, and SQLite databases. A SQLite database connection comes configured for you,\nand standalorm will use it by default if you don\'t add a different one yourself. More on adding database connections can\nbe found in the [documentation](https://standalorm.readthedocs.io).\n\n## Additional Notes\n\nstandalorm is intended for people who are already familiar with Django\'s ORM; as such, the basics of how to use the\nORM are outside the scope of both this README and standalorm\'s [documentation](https://standalorm.readthedocs.io). If you\'re\nlooking to familiarize yourself with Django\'s ORM, see [Django\'s own documentation](https://docs.djangoproject.com/en/3.1/topics/db/),\nparticularly the sections on [models](https://docs.djangoproject.com/en/3.1/topics/db/models/) and [making queries](https://docs.djangoproject.com/en/3.1/topics/db/queries/).\n\n\n## Documentation\n\nstandalorm\'s full documentation can be found at https://standalorm.readthedocs.io.\n\n## Attributions\n\nstandalorm is based on Dan Caron\'s [Django ORM Standalone Template](https://github.com/dancaron/django-orm).\n\n"Django" is a registered trademark of the Django Software Foundation, which does not endorse this software.\n\n## License\n\nstandalorm is released under the MIT License.\n',
    'author': 'Jason Tolbert',
    'author_email': 'jasonalantolbert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jasonalantolbert/standalorm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
