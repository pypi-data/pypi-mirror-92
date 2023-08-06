"""Support for importing and building the package
"""
import os.path as op
import pkgutil


def load_info(name):
    """Loads the docstring from README.rst and version from VERSION

    Recommended usage in top-level __init__.py:

    .. code-block :: python

        from mcot.utils.build import load_info
        __doc__, __version__ = load_info(__name__) 
        del load_info

    Package version and description are kept separate, so that pants can access them

    Args:
        path (List[str]): __path__ object in init.py

    Returns:
        str: description of the package to be stored in docstring
        str: version of the package to be stored in __version__
    """
    description = pkgutil.get_data(name, 'README.rst').decode('utf-8')
    version = pkgutil.get_data(name, 'VERSION').decode('utf-8')
    return description, version