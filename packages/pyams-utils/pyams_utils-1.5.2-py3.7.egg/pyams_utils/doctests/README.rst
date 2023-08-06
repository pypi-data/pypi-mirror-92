===================
PyAMS_utils package
===================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)


Getting interface field doc
---------------------------

PyAMS provides a small helper function used to get a FieldProperty docstring, based on the
definition of it's attached interface field:

    >>> from zope.interface import implementer, Interface
    >>> from zope.schema import TextLine

    >>> class IMyInterface(Interface):
    ...     title1 = TextLine()
    ...     title2 = TextLine(title="Field title")
    ...     title3 = TextLine(title="Field title",
    ...                       description="Field description")

    >>> from zope.schema.fieldproperty import FieldProperty
    >>> @implementer(IMyInterface)
    ... class MyContent:
    ...     title1 = FieldProperty(IMyInterface['title1'])
    ...     title2 = FieldProperty(IMyInterface['title2'])
    ...     title3 = FieldProperty(IMyInterface['title3'])

    >>> from pyams_utils import get_field_doc
    >>> MyContent.title1.__doc__
    '...'
    >>> MyContent.title2.__doc__
    'Field title'
    >>> MyContent.title3.__doc__
    'Field title: Field description'


Tests cleanup:

    >>> tearDown()
