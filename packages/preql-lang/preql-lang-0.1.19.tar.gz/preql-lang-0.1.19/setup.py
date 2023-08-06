# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preql', 'preql.autodoc', 'preql.jup_kernel']

package_data = \
{'': ['*'], 'preql': ['modules/*']}

install_requires = \
['dsnparse',
 'lark-parser>=0.11.1,<0.12.0',
 'prompt-toolkit',
 'pygments',
 'rich>=9.5.1,<10.0.0',
 'runtype>=0.1.6,<0.2.0',
 'tqdm']

extras_require = \
{'mysql': ['mysqlclient'], 'pgsql': ['psycopg2'], 'server': ['starlette']}

entry_points = \
{'console_scripts': ['preql = preql.__main__:main']}

setup_kwargs = {
    'name': 'preql-lang',
    'version': '0.1.19',
    'description': 'An interpreted relational query language that compiles to SQL',
    'long_description': '![alt text](logo_small.png "Logo")\n\nPreql (*pronounced: Prequel*) is an interpreted, relational programming language, that specializes in database queries.\n\nIt is designed for use by data engineers, analysts and data scientists.\n\nPreql\'s main objective is to provide an alternative to SQL, in the form of a high-level programming language, with first-class functions, modules, strict typing, and Python integration.\n\n**How does it work?**\n\nPreql code is interpreted and gets compiled to SQL at runtime. This way, Preql gains the performance and abilities of SQL, but can also operate as a normal scripting language.\n\nCurrently supported dialects are:\n* Postgres\n* MySQL\n* Sqlite\n* BigQuery (soon)\n* More... (planned)\n\nFor features that are database-specific, or aren\'t implemented in Preql, there is a `SQL()` function that provides a convenient escape hatch to write raw SQL code.\n\n**Main Features**\n\n* Modern syntax and semantics\n    - Interpreted, everything is an object\n    - Strong type system with gradual type validation and duck-typing\n* Compiles to SQL\n* Python and Pandas integration\n* Interactive shell (REPL) with auto-completion\n* Runs on Jupyter Notebook\n\n\n**Note: Preql is still work in progress, and isn\'t ready for production use, or any serious use quite yet.**\n\n# Learn More\n\n- [**Read the documentation**](https://preql.readthedocs.io/en/latest/)\n\n- [Follow the tutorial](https://preql.readthedocs.io/en/latest/tutorial.html)\n\n- [Browse the examples](https://github.com/erezsh/Preql/tree/master/examples)\n\n\n# Get started\n\nSimply install via pip:\n\n```sh\n    pip install -U preql-lang\n```\n\nThen just run the interpreter:\n\n```sh\n    preql\n```\n\nRequires Python 3.8+\n\n[Read more](https://preql.readthedocs.io/en/latest/getting-started.html)\n\n# Quick Example\n\n```javascript\n// The following code sums up all the squares of an aggregated list of\n// numbers, grouped by whether they are odd or even.\n\nfunc sum_of_squares(x) = sum(x * x)\nfunc is_even(x) = (x % 2 == 0)\n\n// Create a list of [1, 2, 3, ..., 99]\nnum_list = [1..100]\n\n// Group by is_even(), and run sum_of_squares() on the grouped values.\nprint num_list{ is_even(item) => sum_of_squares(item) }\n\n// Result is:\n┏━━━━━━━━━┳━━━━━━━━┓\n┃ is_even ┃ sqrsum ┃\n┡━━━━━━━━━╇━━━━━━━━┩\n│       0 │ 166650 │\n│       1 │ 161700 │\n└─────────┴────────┘\n```\n\nIn the background, this was run by executing the following compiled SQL code (reformatted):\n\n```sql\n  WITH range1 AS (SELECT 1 AS item UNION ALL SELECT item+1 FROM range1 WHERE item+1<100)\n  SELECT ((item % 2) = 0) AS is_even, SUM(item * item) AS sqrsum FROM range1 GROUP BY 1;\n```\n\n# License\n\nPreql uses an “Interface-Protection Clause” on top of the MIT license.\n\nSee: [LICENSE](LICENSE)\n\nIn simple words, it can be used for any commercial or non-commercial purpose, as long as your product doesn\'t base its value on exposing the Preql language itself to your users.\n\nIf you want to add the Preql language interface as a user-facing part of your commercial product, contact us for a commercial license.\n',
    'author': 'Erez Shin',
    'author_email': 'erezshin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erezsh/Preql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
