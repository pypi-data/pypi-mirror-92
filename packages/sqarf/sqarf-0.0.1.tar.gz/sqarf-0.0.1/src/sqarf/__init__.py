from ._version import get_versions

from .qatest import QATest
from .session import Session

__version__ = get_versions()["version"]
del get_versions
