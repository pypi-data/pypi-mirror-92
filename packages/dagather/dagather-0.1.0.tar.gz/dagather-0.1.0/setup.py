# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dagather']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dagather',
    'version': '0.1.0',
    'description': 'directed acyclic gather',
    'long_description': "# Dagather\ndagather (**d**irected **a**cyclic **gather**) is a new way to plan out and schedule asynchronous tasks. The tasks are organized, with each task specifying the tasks that come before it. The tasks are then run in topological order, ensuring that each operation will start as soon as it is able to without waiting for routines it does not need.\n\n```python\nfrom asyncio import sleep\nfrom dagather import Dagather\n\nfoo = Dagather()\n\n@foo.register\n# add a new task to the task list\nasync def a():\n    await sleep(1)\n    return 12\n\n@foo.register\nasync def b(a):\n    # we now specify that a is a requirement for this task,\n    # meaning that b will not be called until a has finished.\n    # during runtime, a's value will be the return value of the\n    # a task\n    assert a == 12\n    await sleep(2)\n\n@foo.register\nasync def c(a):\n    await sleep(1)\n    return 'testing'\n\n@foo.register\nasync def d():\n    await sleep(1)\n\n@foo.register\nasync def e(d, c):\n    await sleep(1)\n\nresult = await foo()\n# when foo is called, it runs each of its registered tasks \n# as soon as all its dependencies are finished.\n# once all the tasks are finished, it will return a dict\n# mapping each task to its return value.\nassert result == {\n    a: 12,\n    b: None,\n    c: 'testing',\n    d: None,\n    e: None\n}\n```",
    'author': 'ben avrahami',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bentheiii/dagather',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
