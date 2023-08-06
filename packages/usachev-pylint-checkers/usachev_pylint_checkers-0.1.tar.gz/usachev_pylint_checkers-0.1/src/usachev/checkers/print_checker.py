from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from astroid.node_classes import Name


class PrintChecker(BaseChecker):
    __implements__ = IAstroidChecker

    CODE = "forbidden-print-statement"

    name = 'forbidden_print_statement'
    priority = -1
    msgs = {
        'W0080': (
            'Code contains print statement',
            CODE,
            'Remove print statement'
        ),
    }

    def __init__(self, linter=None):
        super().__init__(linter)

    def visit_call(self, node):
        func = node.func
        if isinstance(func, Name) and func.name == "print":
            self.add_message(PrintChecker.CODE, node=node)


def register(linter):
    linter.register_checker(PrintChecker(linter))
