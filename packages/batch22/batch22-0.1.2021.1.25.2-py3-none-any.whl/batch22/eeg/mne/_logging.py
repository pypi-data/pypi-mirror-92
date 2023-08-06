#!/usr/bin/env python
# -*- coding: utf-8 -*


import logging

import datetime as dt
from pytz import timezone as tz
loc_tz = tz("Europe/Berlin")

import mne
mne.set_log_level("INFO")
mne.set_log_level("WARNING")

from ._indent import indS,indD,indN,indB


def setup_logger(self,idstr):
    ## Setup the logger
    self.logging = logging
    self.logger  = logging.getLogger(__name__)
    """
    self.logger.setLevel(logging.CRITICAL) # 50
    self.logger.setLevel(logging.ERROR)    # 40
    self.logger.setLevel(logging.WARNING)  # 30
    self.logger.setLevel(logging.INFO)     # 20
    self.logger.setLevel(logging.DEBUG)    # 10
    self.logger.setLevel(logging.NOTSET)   # 00
    """
    self.handler0 = logging.StreamHandler()
    self.handler0.setFormatter(
        logging.Formatter(" ".join([
            # "%(asctime)s",
            # "%(name)s",
            "%(levelname).1s:",
            # "%(module)s",
            "%(funcName)-16s ",
            "%(message)s",
        ]),
        datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    fn0 = self.logger_dir/(dt.datetime.now(loc_tz).strftime("%Y%m%d_%H%M%S_%f")[:-3]+idstr+".log")
    self.handler1 = logging.FileHandler(fn0)
    self.handler1.setFormatter(
        logging.Formatter(" ".join([
            "%(asctime)s",
            # "%(name)s",
            "%(levelname).1s:",
            # "%(module)s",
            "%(funcName)-16s ",
            "%(message)s",
        ]),
        datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    self.logger  .setLevel(logging.DEBUG)
    self.handler0.setLevel(logging.INFO)
    self.handler1.setLevel(logging.DEBUG)

    for handler in self.logger.handlers[:]: self.logger.removeHandler(handler)
    self.logger.addHandler(self.handler0)
    self.logger.addHandler(self.handler1)

    ## Also attach MNE logger
    temp_attach_MNE_logger = False
    temp_attach_MNE_logger = True
    if temp_attach_MNE_logger:
        for handler in mne.utils.logger.handlers[:]: mne.utils.logger.removeHandler(handler)
        mne.utils.logger.setLevel(logging.DEBUG)
        mne.utils.logger.addHandler(self.handler0)
        mne.utils.logger.addHandler(self.handler1)

    self.logger.info (indS(0)+"logging to: "+str(fn0))
    self.logger.debug(indS(0)+"handler0 level: "+str(logging.getLevelName(self.handler0)))
    self.logger.debug(indS(0)+"handler1 level: "+str(logging.getLevelName(self.handler1)))
    self.logger.info (indS(0)+"MNE version: " + str(mne.__version__))
