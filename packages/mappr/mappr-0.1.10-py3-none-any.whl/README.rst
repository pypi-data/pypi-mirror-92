.. readme_badges_start

|circleci| |nbsp| |codecov| |nbsp| |mypy| |nbsp| |license| |nbsp| |py_ver|


.. |circleci| image:: https://circleci.com/gh/novopl/mappr.svg?style=shield
                :target: https://circleci.com/gh/novopl/mappr
.. |codecov| image:: https://codecov.io/gh/novopl/mappr/branch/master/graph/badge.svg?token=SLX4NL21H9
                :target: https://codecov.io/gh/novopl/mappr
.. |mypy| image:: https://img.shields.io/badge/type_checked-mypy-informational.svg
.. |license| image:: https://img.shields.io/badge/License-Apache2-blue.svg
.. |py_ver| image:: https://img.shields.io/badge/python-3.7+-blue.svg
.. |nbsp| unicode:: 0xA0

.. readme_badges_end

#####
mappr
#####


Easily convert between arbitrary types.


Goals
=====

.. readme_about_start

**mappr**'s goal is to make it as easy as possible to define custom converters
between arbitrary types in python. It does not concern itself with validation
or coercion. It only provides a simple way to define a mapping between two
types + some extra functionality to automatically generate converters for simple
cases (off by default).

.. readme_about_end

.. note::

    Python 3.6 support will be added soon (need to make dataclasses an
    optional import).

Links
=====

* `Documentation`_

    * `Contributing`_
    * `Reference`_


.. _Documentation: https://novopl.github.io/mappr
.. _Contributing: https://novopl.github.io/mappr/pages/contributing.html
.. _Reference: https://novopl.github.io/mappr/pages/reference.html


Installation
============

.. readme_installation_start

.. code-block:: shell

    $ pip install mappr

or if you're using poetry.

.. code-block:: shell

    $ poetry add mappr

.. readme_installation_end


Quick Example
=============

See the `Documentation`_ for more examples.

.. readme_example_start

Assume we have a following types in our app. They represent pretty much the same
thing, but different views of it.

.. code-block:: python

    from dataclasses import dataclass
    import mappr

    @dataclass
    class User:
        username: str
        first_name: str
        last_name: str
        email: str

    @dataclass
    class Person:
        nick: str
        name: str
        email: str


    mappr.register(User, Person, mapping=dict(
        nickname=lambda obj, name: obj.nick,
        name=lambda obj, name: f"{obj.first_name} {obj.last_name}",
    ))

    user = User(
        username='john.doe',
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
    )

    assert mappr.convert(Person, user) == Person(
        name='John Doe',
        email='john.doe@example.com',
        nick='john.doe',
    )

.. readme_example_end
