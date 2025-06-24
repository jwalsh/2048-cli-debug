"""TTY-based 2048 controller package"""

__version__ = "0.1.0"

from .tty_reader import TTYReader
from .board_analyzer import BoardAnalyzer
from .manual_test_runner import ManualTestRunner

__all__ = ["TTYReader", "BoardAnalyzer", "ManualTestRunner"]