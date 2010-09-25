"""Gomill-specific test support code."""

from gomill_tests import test_framework

from gomill.gomill_common import *
from gomill import ascii_boards
from gomill import boards

def check_boards_equal(b1, b2):
    """Check that two boards are equal.

    Does nothing if they are equal; raises ValueError with a message if they
    are not.

    """
    if b1.side != b2.side:
        raise ValueError("size is different: %s, %s" % (b1.side, b2.side))
    differences = []
    for row, col in b1.board_coords:
        if b1.get(row, col) != b2.get(row, col):
            differences.append((row, col))
    if not differences:
        return
    msg = "boards differ at %s" % " ".join(map(format_vertex, differences))
    try:
        msg += "\n%s\n%s" % (
            ascii_boards.render_board(b1), ascii_boards.render_board(b2))
    except Exception:
        pass
    raise ValueError(msg)

class Gomill_testcase_mixin(object):
    """TestCase mixin adding support for gomill-specific types.

    This adds:
     assertBoardEqual
     assertEqual and assertNotEqual for Boards

    """
    def init_gomill_testcase_mixin(self):
        self.addTypeEqualityFunc(boards.Board, self.assertBoardEqual)

    def _format_message(self, msg, standardMsg):
        # This is the same as _formatMessage from unittest2; copying it
        # because it's not part of the public API.
        if not self.longMessage:
            return msg or standardMsg
        if msg is None:
            return standardMsg
        try:
            return '%s : %s' % (standardMsg, msg)
        except UnicodeDecodeError:
            return '%s : %s' % (unittest2.util.safe_str(standardMsg),
                                unittest2.util.safe_str(msg))

    def assertBoardEqual(self, b1, b2, msg=None):
        try:
            check_boards_equal(b1, b2)
        except ValueError, e:
            self.fail(self._format_message(msg, str(e)+"\n"))

    def assertNotEqual(self, first, second, msg=None):
        if isinstance(first, boards.Board) and isinstance(second, boards.Board):
            try:
                check_boards_equal(first, second)
            except ValueError:
                return
            msg = self._format_message(msg, 'boards have the same position')
            raise self.failureException(msg)
        super(Gomill_testcase_mixin, self).assertNotEqual(first, second, msg)

class Gomill_SimpleTestCase(
    Gomill_testcase_mixin, test_framework.SimpleTestCase):
    """SimpleTestCase with the Gomill mixin."""
    def __init__(self, *args, **kwargs):
        test_framework.SimpleTestCase.__init__(self, *args, **kwargs)
        self.init_gomill_testcase_mixin()


def make_simple_tests(source, prefix="test_"):
    """Make test cases from a module's test_xxx functions.

    See test_framework for details.

    The test functions can use the Gomill_testcase_mixin enhancements.

    """
    return test_framework.make_simple_tests(
        source, prefix, testcase_class=Gomill_SimpleTestCase)
