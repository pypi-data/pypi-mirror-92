__version__ = 0.1

from pylint.utils import register_plugins


def register(linter):
    initialize(linter)


def initialize(linter):
    """initialize linter with checkers in this package """
    register_plugins(linter, __path__[0])

