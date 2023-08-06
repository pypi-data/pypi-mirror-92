#!/usr/bin/env python
# -*- coding: utf-8 -*

import re
import pathlib

from ._indent import indS,indD,indN,indB
from ._whoami import whoami

class LocsMNE():
    def __init__(self,stack,file0,BATCH):
        self.name     = "locs"
        self.stack    = stack+"."+self.name
        self.file0    = file0
        self.BATCH    = BATCH
        self.logger   = BATCH.logger

        self.id_path  = self.BATCH.source_dir
        self.if_path  = file0.relpath.split(".")[0]
        self.if_extn  = file0.relpath.split(".",1)[1]
        self.if_path  = re.sub(r"_run-\d\d\d_eeg","_run-000_eeg",self.if_path)
        self.if_path  = (self.id_path/self.if_path).with_suffix(".{}".format(self.if_extn))
        self.of_path  = self.BATCH.target_dir / self.if_path.relative_to(self.BATCH.source_dir)
        self.od_path  = self.of_path.parents[0]
        self.of_stem  = pathlib.Path(self.of_path.stem.split('.')[0])
        self.of_base  = self.od_path / self.of_stem
        self.of_data  = self.of_base.with_suffix(".gzip.hkl")
        self.of_done  = self.of_base.with_suffix(".{}".format(self.BATCH.done_ext))

    def __str__(self):
        return self._str()

    def __repr__(self):
        return self._str()

    def _str(self):
        out_str  = ""
        out_str += indS(0)+self.stack+" <{}>:".format(type(self).__name__)
        out_str += indN(1)+"id_path = {}".format(repr(str( self.id_path )))
        out_str += indN(1)+"if_path = {}".format(repr(str( self.if_path )))
        out_str += indN(1)+"of_path = {}".format(repr(str( self.of_path )))
        out_str += indN(1)+"od_path = {}".format(repr(str( self.od_path )))
        out_str += indN(1)+"of_stem = {}".format(repr(str( self.of_stem )))
        out_str += indN(1)+"of_base = {}".format(repr(str( self.of_base )))
        out_str += indN(1)+"of_data = {}".format(repr(str( self.of_data )))
        out_str += indN(1)+"of_done = {}".format(repr(str( self.of_done )))
        return out_str

    def info(self):
        print(self.__str__())

    def INFO(self):
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        out_str = self.__str__()
        for line0 in out_str.split("\n"): self.logger.info(line0)
