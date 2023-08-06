#!/usr/bin/env python
# -*- coding: utf-8 -*


import os
from pathlib import Path
import contextlib
from contextlib import ExitStack
import pandas as pd

def cont_pd(
        max_columns  =  45,
        max_colwidth =  80,
        width        = 800,
        max_rows     =  45,
        min_rows     =  45,
):
    """Replace multiple nested with statements using one ExitStack.

    Example use:

      import pandas as pd
      from contextlib import ExitStack
      import batch22 as b22
      from batch22.eeg.mne._contexts import cont_pd

      with ExitStack() as stack:
        [stack.enter_context(cont) for cont in cont_pd()]
        print( pd.get_option("display.max_rows") )
        # display(df2)

"""

    return [
        pd.option_context("display.max_columns"  , max_columns  ),
        pd.option_context("display.max_colwidth" , max_colwidth ),
        pd.option_context("display.width"        , width        ),
        pd.option_context("display.max_rows"     , max_rows     ),
        pd.option_context("display.min_rows"     , min_rows     ),
    ]


@contextlib.contextmanager
def cwdc(path):
    """Changes working directory and returns to previous on exit.

    Example:

      import os
      from batch22.eeg.mne._contexts import cwdc
      from pathlib import Path

      print(os.getcwd())
      with cwdc(Path.home()):
        print(os.getcwd())

    """
    cwd0 = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd0)
