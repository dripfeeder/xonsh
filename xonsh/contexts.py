"""Context management tools for xonsh."""
import builtins

from xonsh.tools import XonshBlockError

class Block(object):
    """This is a context manager for obtaining a block of lines without actually
    executing the block. The lines are accessible as the 'lines' attribute.
    """
    __xonsh_block__ = True

    def __init__(self, lines=None):
        """
        Attributes
        ----------
        lines : list of str or None
            Block lines as if split by str.splitlines(), if available.
        glbs : Mapping or None
            Global execution context, ie globals().
        locs : Mapping or None
            Local execution context, ie locals().
        """
        self.lines = self.glbs = self.locs = None

    def __enter__(self):
        self.lines = self.glbs = self.locs = None  # make re-entrant
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not XonshBlockError:
            return  # some other kind of error happened
        self.lines = exc_value.lines
        self.glbs = exc_value.glbs
        if exc_value.locs is not self.glbs:
            # leave locals as None when it is the same as globals
            self.locs = exc_value.locs
        return True