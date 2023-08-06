#!/usr/bin/env python
# -*- coding: utf-8 -*

import inspect


def whoami():
    """
    Example usage

      def foo():
          print(whoami())

      foo()

    """

    # frame = inspect.currentframe()
    # frame = inspect.currentframe().f_back.f_code
    frame = inspect.currentframe().f_back
    return str(inspect.getframeinfo(frame).function)
