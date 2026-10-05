"""The two errors a command reports instead of a result."""


class ToolError(Exception):
    """A usage or environment problem: not a git repository, no bundle, a schema
    mismatch. The command exits 2."""


class Refused(Exception):
    """The command will not act on this state, for example a key that is already
    merged. The command exits 1."""
