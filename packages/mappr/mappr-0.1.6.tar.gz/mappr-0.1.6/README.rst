###############################################
mappr - Easily convert between arbitrary types.
###############################################

.. readme_about_start

**mappr**'s goal is to make it as easy as possible to define custome converters
between arbitrary types in python. It does not concern itself with validation
or coercion. It only provides a simple way to define a mapping between two
types + some extra functionality to automatically generate converters for simple
cases (off by default).

.. readme_about_end


Links
=====

- `Documentation`_
    - `Contributing`_
    - `Reference`_
- `Source Code`_

.. _Documentation: https://novopl.github.io/mappr
.. _Contributing: https://novopl.github.io/mappr/pages/contributing.html
.. _Reference: https://novopl.github.io/mappr/pages/reference.html
.. _Source Code: https://github.com/novopl/mappr


Installation
============

.. readme_installation_start

.. code-block:: shell

    $ pip install mappr

or if you're using poetry.

.. code-block:: shell

    $ poetry add mappr

.. readme_installation_end


Example
=======

.. readme_example_start

Assume we have a following types in our app. They represent pretty much the same
thing, but different views of it.

.. code-block:: python

    from dataclasses import asdict, dataclass
    from typing import Any

    import mappr

    # A few sample models to demonstrate mappr.
    @dataclass
    class Person(Base):
        name: str
        surname: str
        email: str
        nickname: str

    @dataclass
    class User(Base):
        username: str
        first_name: str
        last_name: str
        email: str

    @dataclass
    class UserPublic(Base):
        username: str
        first_name: str


We can register a mapper from ``User`` to ``Person``. Fields not specified in
mapping will be copied directly. The source type needs the have attributes
that match the name, otherwise an exception is raised.

.. code-block:: python

    mappr.register(User, Person, mapping=dict(
        nickname=lambda obj, name: obj.nickname,
        name=lambda obj, name: obj.first_name,
        surname=lambda obj, name: obj.last_name,
    ))

We can now create a an instance of ``User`` so we can test our converter.

.. code-block:: python

    user = User(
        username='john.doe',
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
    )

This will use the converter registered above. To allow conversion in the
reverse direction, you need to register the appropriate converter first.
Each converter works only one way.

.. code-block:: python

    assert mappr.convert(Person, user) == Person(
        name='John',
        surname='Doe',
        email='john.doe@example.com',
        nickname='john.doe',
    )

For simple conversions, where the target type attributes are a subset of
source's attributes, we can just pass ``strict=False`` to let mappr create
an ad-hoc converter. This will only work if the attribute names are
exactly the same.

.. code-block:: python

    assert mappr.convert(UserPublic, user, strict=False) == UserPublic(
        username='John',
        first_name='john.doe',
    )

.. readme_example_end
