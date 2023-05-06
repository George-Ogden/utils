try:
    from typing import Self
    # use Self for Python>=3.11
except ImportError:
    Self = "Self"
    # define Self for Python<3.11