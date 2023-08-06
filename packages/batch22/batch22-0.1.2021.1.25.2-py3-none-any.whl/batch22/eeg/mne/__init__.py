#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
TODO:
- [ ] save time by keeping separate channel and bundle based epochs/evokeds

FUTURAMA:
- [ ] allow to pickle (for the purpose of parallel processing using MNE.parallel)


"""

import os
import sys
import glob
import pathlib
import shutil
import uuid

import json
import numpy  as np
import pandas as pd
import hickle as hkl

import bids
from bids import BIDSLayout

from scipy import ndimage
from scipy.signal import find_peaks,peak_prominences

import itertools

from copy import deepcopy as dc


import time
import datetime as dt
from pytz import timezone as tz
loc_tz = tz("Europe/Berlin")
import humanfriendly as hf

from pprint import pprint  as pp
from pprint import pformat as pf

import collections
from collections import OrderedDict
from collections import UserDict
# from dotmap import DotMap


import deepsensemaking as dsm
from deepsensemaking.bids  import get_bids_prop
from deepsensemaking.dicts import str_dict,print_dict


import matplotlib
from matplotlib import pyplot as plt
from matplotlib.pyplot import imshow
from matplotlib.colors import ListedColormap
plt.ion()
matplotlib.rcParams['figure.dpi'] = 150


import seaborn as sns


from ._indent   import indS,indD,indN,indB
from ._whoami   import whoami
from ._contexts import cont_pd

from contextlib import ExitStack


import mne

from autoreject import AutoReject,get_rejection_threshold,set_matplotlib_defaults
from autoreject import Ransac
from autoreject.utils import interpolate_bads  # noqa


class BatchMNE(UserDict):
    """MNE batch job class...
    (AKA: duct-tape + cable-ties for EEG preprocessing)
    Example usage:

      from   batch22.eeg.mne import BatchMNE
      sdf0 = BatchMNE(
        name       = "sdf0",
        metadata   = "inputs/metadata/metadata.json",
        includes   = "inputs/metadata/includes.json",
        source_ext = "vhdr",
        source_dir = "inputs/rawdata/",
        target_dir = "outputs/st.0101/",
        target_ext = "",
        done_ext   = "done",
      )
      # self = sdf0
      sdf0.get_data()
      sdf0.info()

      self = sdf0["37lpxm"]

      self.info()
      self.info(2)

    """
    def __init__(
            self,
            name       = "fds0",
            metadata   = "inputs/metadata/metadata.json",
            includes   = "inputs/metadata/includes.json",
            source_ext = "vhdr",
            source_dir = "inputs/rawdata/",
            target_dir = "outputs/st.0101/",
            target_ext = "",
            done_ext   = "done", # TODO FIXME rename to finito_ext
    ):

        ## Initialize using super-class
        UserDict.__init__(self)

        bids.config.set_option('extension_initial_dot', True)

        ## Ensure paths are of type pathlib.Path
        metadata   = pathlib.Path(metadata)
        includes   = pathlib.Path(includes)
        source_dir = pathlib.Path(source_dir)
        target_dir = pathlib.Path(target_dir)

        ## Initial assertions
        assert source_dir.is_dir(),"PROBLEM: source_dir ({}) not found or not a directory".format(source_dir)
        assert metadata.is_file(),"PROBLEM: metadata file ({}) does not exist".format(metadata)
        assert includes.is_file(),"PROBLEM: includes file ({}) does not exist".format(includes)
        test0 = {"name":name,"source_ext":source_ext,"done_ext":done_ext}
        for key0,val0 in test0.items():
            assert isinstance(val0,(str,)),"PROBLEM: '{}' is not a string ({})".format(key0,str(type(val0)))

        ## Initial values
        self.name       = name
        self.metadata   = metadata
        self.includes   = includes
        self.source_ext = source_ext
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.target_ext = target_ext
        self.logger_dir = target_dir/"logs"
        self.done_ext   = done_ext
        self.uuid4      = str(uuid.uuid4())
        self.stack      = str(name)
        self.layout     = None
        self.meta       = OrderedDict()
        self.incl       = OrderedDict()
        self.group      = OrderedDict()
        self.meta_meths()
        self.incl_meths()
        self.group_meths()
        self.target_dir.mkdir(mode=0o700,parents=True,exist_ok=True)
        self.logger_dir.mkdir(mode=0o700,parents=True,exist_ok=True)
        from ._logging import setup_logger
        setup_logger(self,self.uuid4)
        self.logger.info(indS(0)+"{} <{}> was casted, NICE!".format(self.name,type(self).__name__,))

    def keys(self):   return self.data.keys()   # TODO: check this solution against ABC and COLLECTIONS
    def vals(self):   return self.data.values() # TODO: check this solution against ABC and COLLECTIONS
    def values(self): return self.data.values() # TODO: check this solution against ABC and COLLECTIONS
    def items(self):  return self.data.items()  # TODO: check this solution against ABC and COLLECTIONS

    def __str__ (self): return str_dict(self.data,indS(1)+self.name,disp_types=None,tight=True)
    def __repr__(self): return str_dict(self.data,indS(1)+self.name,disp_types=None,tight=True)
    def _str(self):
        out_str  = ""
        out_str += indS(0)+"{} <{}>:".format(self.name,type(self).__name__,)
        out_str += indN(1)+self.name+".name       = "+repr(str( self.name       ))
        out_str += indN(1)+self.name+".metadata   = "+repr(str( self.metadata   ))
        out_str += indN(1)+self.name+".includes   = "+repr(str( self.includes   ))
        out_str += indN(1)+self.name+".source_ext = "+repr(str( self.source_ext ))
        out_str += indN(1)+self.name+".source_dir = "+repr(str( self.source_dir ))
        out_str += indN(1)+self.name+".target_dir = "+repr(str( self.target_dir ))
        out_str += indN(1)+self.name+".target_ext = "+repr(str( self.target_ext ))
        out_str += indN(1)+self.name+".logger_dir = "+repr(str( self.logger_dir ))
        out_str += indN(1)+self.name+".done_ext   = "+repr(str( self.done_ext   ))
        out_str += indN(1)+self.name+".uuid4      = "+repr(str( self.uuid4      ))
        out_str += indN(1)+self.name+".logger     : "+repr(     self.logger      )
        out_str += indN(1)+self.name+".layout     : "+"<{}>".format(self.layout  )
        out_str += indN(1)+self.name+".data       : "+"<{} DataMNE items>".format(len(self.data))
        return out_str

    def info(self):
        print(self._str())

    def INFO(self,out_str=None):
        """Send multi-line string to logger.info().
        If no out_str provided BatchMNE info will be logged.
        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        if out_str is None: out_str = self._str()
        for line0 in out_str.split("\n"): self.logger.info(line0)

    def meta_meths(self):
        self.meta._str = lambda level=1: str_dict(self.meta,self.name+".meta",level,tight=True)
        self.meta.info = lambda level=1: print(self.meta._str(level))
        self.meta.INFO = lambda level=1: self.INFO(self.meta._str(level))

    def incl_meths(self):
        self.incl._str = lambda level=1: str_dict(self.incl,self.name+".incl",level,tight=True)
        self.incl.info = lambda level=1: print(self.incl._str(level))
        self.incl.INFO = lambda level=1: self.INFO(self.incl._str(level))

    def get_meta(self):
        with open(self.metadata) as fh0:
            self.meta = OrderedDict(json.load(fh0))
            self.meta_meths()

    def get_incl(self):
        with open(self.includes) as fh0:
            self.incl = OrderedDict(json.load(fh0))
            self.incl_meths()

    def get_layout(self):
        self.layout = BIDSLayout(self.source_dir,validate=False)

    def get_data(self):
        if self.layout is None: self.get_layout()
        if not self.meta: self.get_meta()
        if not self.incl: self.get_incl()
        subjects = self.layout.get(return_type="id",target="subject")
        for subject in subjects:
            files = self.layout.get(
                extension      = self.source_ext.lstrip("."),
                subject        = subject,
            )
            if self.source_ext.lstrip(".") == "vhdr": assert len(files)==4,"PROBLEM: four runs were expected for each participant"
            self[subject] = DataMNE(
                name  = subject,
                stack = self.stack,
                meta  = dc(self.meta),
                incl  = dc(self.incl),
                files = files,
                BATCH = self,
            )


    def keep_data(self,keep):
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))

        assert isinstance(keep,(list,tuple,set,)),"PROBLEM: keep arg should be list,tuple or set, got {}".format(type(keep).__name__)
        self.logger.info(indS(0)+"keep data: {}".format(keep))
        self.data = {key: self.data.get(key,None) for key in keep}
        # Drop Nones introduced by bad keys (subject names that could have been dropped at earlier stages)
        self.data = {key: val for key,val in self.data.items() if val is not None}


    def drop_data(self,drop):
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))

        assert isinstance(drop,(list,tuple,set,)),"PROBLEM: drop arg should be list,tuple or set, got {}".format(type(drop).__name__)
        self.logger.info(indS(0)+"drop data: {}".format(drop))
        self.data = {key: self.data.get(key,None) for key in self.data.keys() if key not in drop}


    def group_meths(self):
        self.group._str = lambda level=1: str_dict(self.group,self.name+".group",level,tight=True)
        self.group.info = lambda level=1: print(self.group._str(level))
        self.group.INFO = lambda level=1: self.INFO(self.group._str(level))


    def export_group_DFs(
            self,
            epochs0,
            df_key,
            suffStr = "",
            altPath = None,
    ):
        """
        sdf0.export_group_DFs(epochs0="epochs0",df_key="FEATS")
        sdf0.export_group_DFs("epochs0","FEATS")

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        if altPath is None:
            od_path = self.target_dir/"exports"/df_key/epochs0
        else:
            od_path = pathlib.Path(altPath)

        od_path.mkdir(mode=0o700,parents=True,exist_ok=True)
        of_suff = ""
        of_suff = ".".join([of_suff,suffStr,"csv"] if suffStr else [of_suff,"csv"])
        of_path = (od_path/"{}_{}".format(df_key,epochs0)).with_suffix(of_suff)

        self.logger.info(indS(0)+"exporting: {}.group[{}][{}]".format(self.stack,df_key,epochs0))
        self.logger.info(indS(0)+"target file: {}".format(str(of_path)))
        self.group[df_key][epochs0].to_csv(of_path,index=False,)


    def map_group_DFs(
            self,
            epochs0,
            df_key,
    ):
        """
        Example:
          sdf0.map_group_DFs(epochs0="epochs0",df_key="FEATS")

          sdf0.group["FEATS"]["epochs0"].tail(n=33)

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        self.group[df_key][epochs0]["later0"] = self.group[df_key][epochs0]["chan0"].map(self.meta["bund"]["base5"]["later0"] )
        self.group[df_key][epochs0]["front0"] = self.group[df_key][epochs0]["chan0"].map(self.meta["bund"]["base5"]["front0"] )
        self.group[df_key][epochs0]["clust0"] = self.group[df_key][epochs0]["chan0"].map(self.meta["bund"]["base5"]["clust0"] )
        self.group[df_key][epochs0]["goodZ"]  = self.group[df_key][epochs0]["subj0"].map(self.incl["good"]["z0"] )
        self.group[df_key][epochs0]["goodJ"]  = self.group[df_key][epochs0]["subj0"].map(self.incl["good"]["j0"] )


    def get_extra_DFs(
            self,
            epochs0,
            df_key,
            if_path,
            filt_chans = True,
            fix_subj27 = True,
    ):
        """
        Example:
          sdf0.get_extra_DFs(
            epochs0="epochs0",
            df_key="FEATS",
            if_path="inputs/bva_peaks0/data/merged.csv",
          )

          sdf0.group.info(5)
          sdf0.group["FEATS"]["epochs0"]
          list(sdf0.group["FEATS"]["epochs0"].columns)
          list(sdf0.group["FEATS"]["epochs0"]["epochs0"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["subj0"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["cond0"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["tmin0"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["chan0"].unique())

          list(sdf0.group["FEATS"]["epochs0"]["goodZ"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["goodJ"].unique())

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        df0 = pd.read_csv(if_path)
        if filt_chans:
            df0 = df0[df0["chan0"].isin(self.meta["bund"]["base3"]["B1"])]

        if fix_subj27:
            df0.replace({"27mwxf":"27zgxf"},inplace=True,)

        self.group[df_key][epochs0] = self.group[df_key][epochs0].append(df0)


    def get_group_DFs(
            self,
            epochs0,
            df_key,
    ):
        """
        get_group_DFs(epochs0,)
          merge (append) dataframes (e.g., df_key="FEATS") for a given
          epochsX across subjects (sdf0 items)

        Example:
          sdf0.get_group_DFs(epochs0="epochs0",df_key="FEATS")

          sdf0.group.info(5)
          sdf0.group["FEATS"]["epochs0"]
          list(sdf0.group["FEATS"]["epochs0"].columns)
          list(sdf0.group["FEATS"]["epochs0"]["subj0"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["cond0"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["tmin0"].unique())

          list(sdf0.group["FEATS"]["epochs0"]["goodZ"].unique())
          list(sdf0.group["FEATS"]["epochs0"]["goodJ"].unique())

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        # Get the first dataframe
        num0 = 0
        while epochs0 not in self[list(self.keys())[num0]].keys():
            num0 += 1
            continue
            if df_key not in self[list(self.keys())[num0]][epochs0].keys():
                num0 += 1

        ds0 = self[list(self.keys())[num0]]
        df0 = ds0[epochs0][df_key]
        self.logger.debug(indS(0)+"Getting columns from DS ({}): {}".format(num0,ds0))
        # Cast an empty dataframe with relevant columns
        DF0 = pd.DataFrame(
            [],
            columns=df0.columns
        )
        # Merge in
        for ds0 in self.values():
            if epochs0 in ds0.keys():
                if df_key in ds0[epochs0].keys():
                    self.logger.info(indS(0)+"MERGING data from DS {}".format(ds0))
                    DF0 = DF0.append(ds0[epochs0][df_key])

        if df_key not in self.group.keys(): self.group[df_key] = OrderedDict()
        self.group[df_key][epochs0] = DF0


    def get_group_EVOKEDS(
            self,
            epochs0,
    ):
        """
        sdf0.get_group_EVOKEDS(epochs0="epochs0")

        sdf0.group.info(5)
        sdf0.group["EVOKEDS"]["epochs0"]

        sdf0.group["EVOKEDS"]["epochs0"]["word"][2].info

        GA = mne.grand_average(sdf0.group["EVOKEDS"]["epochs0"]["verb"])
        GA.plot()

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        if "EVOKEDS" not in self.group.keys(): self.group["EVOKEDS"] = OrderedDict()
        self.group["EVOKEDS"][epochs0] = OrderedDict()
        for ds0 in self.values():
            if epochs0 in ds0.keys():
                if "evokeds" in ds0[epochs0].keys():
                    for cond0,evoked0 in ds0[epochs0]["evokeds"].items():
                        if cond0 not in self.group["EVOKEDS"][epochs0].keys(): self.group["EVOKEDS"][epochs0][cond0] = list()
                        self.group["EVOKEDS"][epochs0][cond0].append(evoked0.copy())


    def get_group_GAs(
            self,
            epochs0,
    ):
        """
        sdf0.get_group_GAs(epochs0="epochs0")

        sdf0.group.info(5)
        sdf0.group["GA"]["epochs0"]

        sdf0.group["GA"]["epochs0"]["word"].info
        sdf0.group["GA"]["epochs0"]["word"].plot()

        joint_kwargs = dict(
            ts_args=dict(time_unit='s'),
            topomap_args=dict(time_unit='s')
        )
        sdf0.group["GA"]["epochs0"]["word"].plot_joint(**joint_kwargs)
        sdf0.group["GA"]["epochs0"]["noun"].plot_joint(**joint_kwargs)
        sdf0.group["GA"]["epochs0"]["verb"].plot_joint(**joint_kwargs)

        sdf0.group["GA"]["epochs0"]["DIFF_1"] = mne.combine_evoked(
            [
                sdf0.group["GA"]["epochs0"]["noun"],
                sdf0.group["GA"]["epochs0"]["verb"],
            ],
            weights=[1.0,-1.0,])

        sdf0.group["GA"]["epochs0"]["DIFF_1"].plot_joint(**joint_kwargs)


        sdf0.group["GA"]["epochs0"]["DIFF_2"] = mne.combine_evoked(
            [
                sdf0.group["GA"]["epochs0"]["noun-F"],
                sdf0.group["GA"]["epochs0"]["noun-M"],
            ],
            weights=[1.0,-1.0,])

        sdf0.group["GA"]["epochs0"]["DIFF_2"].plot_joint(**joint_kwargs)

        """

        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        if "GA" not in self.group.keys(): self.group["GA"] = OrderedDict()
        self.group["GA"][epochs0] = OrderedDict()
        for cond0,evokeds0 in self.group["EVOKEDS"][epochs0].items():
            self.group["GA"][epochs0][cond0] = mne.grand_average(evokeds0)




from ._locs import LocsMNE


class DataMNE(UserDict):
    """
    self = sdf0["18skxm"]
    """
    def __init__(self,name,stack,meta,incl,files,BATCH):
        UserDict.__init__(self)
        self.name     = name
        self.stack    = stack+"[\"{}\"]".format(name)
        self.meta     = meta
        self.incl     = incl
        self.files    = files
        self.BATCH    = BATCH
        self.logger   = BATCH.logger
        self.logging  = BATCH.logging
        self.handler0 = BATCH.handler0
        self.handler1 = BATCH.handler1
        self.uuid4    = BATCH.uuid4
        self.locs     = LocsMNE(self.stack,self.files[0],self.BATCH,)
        self.sub      = get_bids_prop(self.locs.of_stem,"sub",)
        self.ses      = get_bids_prop(self.locs.of_stem,"ses",)
        self.task     = get_bids_prop(self.locs.of_stem,"task",)
        self.run      = get_bids_prop(self.locs.of_stem,"run",)
        self.data     = OrderedDict()
        self.is_done  = lambda: self.locs.of_done.is_file()
        self.set_done = lambda: self.locs.of_done.touch()
        self.not_done = lambda: self.locs.of_done.unlink()
        self.locs.od_path.mkdir(mode=0o700,parents=True,exist_ok=True)

    # def is_done(self): return self.locs.of_done.is_file()

    def keys(self):   return self.data.keys()   # TODO: check this solution against ABC and COLLECTIONS
    def vals(self):   return self.data.values() # TODO: check this solution against ABC and COLLECTIONS
    def values(self): return self.data.values() # TODO: check this solution against ABC and COLLECTIONS
    def items(self):  return self.data.items()  # TODO: check this solution against ABC and COLLECTIONS

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out_str  = ""
        out_str += "{} [{}] ({}) <{}>".format(
            self.name,
            "----" if self.is_done() else "TODO",
            len(self),
            type(self).__name__,
        )
        return out_str

    def __len__(self):
        return len(self.data.keys())

    def _str(self,level=None):
        out_str  = ""
        out_str += indS(0)+self.__str__()
        if level is not None: out_str += indN(0)+str_dict(self.data,indS(1)+self.stack,level,tight=True)
        return out_str

    def info(self,level=1):
        print(self._str(level=level))

    def INFO(self,level=1,out_str=None):
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        if out_str is None: out_str = self._str(level=level)
        for line0 in out_str.split("\n"): self.logger.info(line0)


    def get_files(
            self,
            files0,
    ):
        """
        Example use:
          self.get_files(files0="files0")
          self.info()
          self["files0"]
        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        self[files0] = [self.locs.id_path/file0.relpath for file0 in self.files]


    def assert_files(
            self,
            files0,
    ):
        """
        Example use:
          import pathlib
          self.assert_files(files0="files0")
          self["files0"][0] = pathlib.Path("nonexistent")
          self.assert_files(files0="files0")

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        for file0 in self[files0]:
            assert file0.is_file(),"PROBLEM: file \"{}\" not found!".format(str(file0))


    def read_raw_data_list(
            self,
            raws0,
            files0,
            preload = True,
            verbose = None,
    ):
        """
        Example use:
          self.read_raw_data_list(
            raws0   = "raws0",
            files0  = "files0",
            preload = True,
            verbose = None,
          )
          self.info()
          self["raws0"]["run1"].info["description"]

        Example test:
          get_ipython().magic("load_ext autoreload")
          get_ipython().magic("autoreload 2")
          from batch22.eeg.mne import *
          sdf0 = BatchMNE()
          sdf0.get_data()
          self = sdf0["37lpxm"]
          self.get_files(files0="files0")
          self.assert_files(files0="files0")

          self.read_raw_data_list(
            raws0   = "raws0",
            files0  = "files0",
            preload = True,
            verbose = None,
          )
          self.info()
          self["raws0"]["run1"].info["description"]

          raw0 = self["raws0"]["run1"]

          raws0   = "raws0"
          files0  = "files0"
          preload = True
          verbose = None


        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        self[raws0] = OrderedDict()
        for file0 in self[files0]:
            self.logger.info(indS(1)+"RUN: {}(...)".format("mne.io.read_raw_brainvision"))
            ARGS = dict(
                vhdr_fname = file0,
                eog        = ['HEOGL','HEOGR','VEOGb'],
                misc       = 'auto',
                scale      = 1.0,
                preload    = preload,
                verbose    = verbose,
            )
            for line in str_dict(ARGS,indD(1)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)
            raw0 = mne.io.read_raw_brainvision(
                **ARGS,
            )
            raw0.info["description"] = str(file0)
            key0 = "run{}".format(str(int(get_bids_prop(file0,"run"))))
            self[raws0][key0] = raw0.copy()


    def set_raws_montages(
            self,
            raws0,
            montage,
            match_case = True,
    ):
        """
        Example use:
          self.set_raws_montages(
            raws0   = "raws0",
            montage = self.meta["montage"],
          )
          self["raws0"]["run1"].get_montage()

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        for key0,raw0 in self[raws0].items():
            self.logger.info(indS(1)+"RUN: {}.{}(...)".format(self.stack,"set_montage"))
            self.logger.info(indS(1)+"NOW: {}".format(key0))
            ARGS = dict(
                montage    = montage,
                match_case = match_case,
            )
            for line in str_dict(ARGS,indD(1)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)
            raw0.set_montage(
                **ARGS,
            )


    def set_raws_reference(
            self,
            raws0,
            ref_chans_NEW = "average",
            projection    = True,
            ch_type       = "eeg",
    ):
        """
        Example use:

          self.set_raws_reference(raws0="raws0")

          self.set_raws_reference(
            raws0         = "raws0",
            ref_chans_NEW = "average",
            projection    = True,
            ch_type       = "eeg",
          )
          self["raws0"]["run1"]
          self["raws0"]["run1"].info["custom_ref_applied"]
          self["raws0"]["run1"].info["projs"]

        TODO: Do more chekups on this one
        TODO: SEE: https://github.com/mne-tools/mne-python/issues/3998
        TODO: CHECK: when projection=False two re-referencing procedures
        are applied (the second is "custom")

        Testing:
          raw0 = self["raws0"]["run1"].copy()
          raw1 = self["raws0"]["run1"].copy()
          raw2 = self["raws0"]["run1"].copy()
          raw3 = self["raws0"]["run1"].copy()

          raw1.set_eeg_reference("average",False)
          raw2.set_eeg_reference("average",True)
          raw3.set_eeg_reference("average",True)
          raw3.apply_proj()

          raw0.plot()
          raw1.plot()
          raw2.plot()
          raw3.plot()

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        for key0,raw0 in self[raws0].items():
            self.logger.info(indS(1)+"RUN: {}.{}(...)".format(self.stack,"set_eeg_reference"))
            self.logger.info(indS(1)+"NOW: {}".format(key0))
            ARGS = dict(
                ref_channels = ref_chans_NEW,
                projection   = projection,
                ch_type      = ch_type,
            )
            for line in str_dict(ARGS,indD(1)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)
            raw0.set_eeg_reference(
                **ARGS,
            )
            raw0.apply_proj()


    def filter_raws(
            self,
            raws0,
            l_freq,
            h_freq,
            fir_design,
    ):
        """
        Example use:
          self.filter_raws(
            raws0      = "raws0",
            l_freq     = self.meta["filt"]["l_freq"],
            h_freq     = self.meta["filt"]["h_freq"],
            fir_design = self.meta["filt"]["fir_design"],
          )
          self["raws0"]["run1"].info["highpass"]
          self["raws0"]["run1"].info["lowpass"]
          self["raws0"]["run1"].info
        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        for key0,raw0 in self[raws0].items():
            self.logger.info(indS(1)+"RUN: {}.{}(...)".format(self.stack,"filter"))
            self.logger.info(indS(1)+"NOW: {}".format(key0))
            ARGS = dict(
                l_freq     = l_freq,
                h_freq     = h_freq,
                fir_design = fir_design,
            )
            for line in str_dict(ARGS,indD(1)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)
            raw0.filter(
                **ARGS,
            )


    def construct_epochs(
            self,
            epochs0,
            raws0,
            tmin     = -0.200,
            tmax     =  0.900,
            baseline = (None, 0),
            export   = True,
    ):
        """
        Example use:
          self.construct_epochs(
            epochs0  = "epochs0",
            raws0    = "raws0",
            tmin     = -0.200,
            tmax     =  0.900,
            baseline = (None, 0),
          )
          self.info(2)
          str(self["epochs0"]["run1"]["data"]).split("\n")[0]

          self["epochs0"]["run1"]["data"]
          self["epochs0"]["run3"]["data"]

          self["epochs0"]["run0"]["data"]

        Testing:
          epochs0 = "epochs0"
          key0 = "run3"
          raw0 = self["raws0"][key0].copy()

          epo0 = self["epochs0"]["run0"]["data"]
          raw1 = self["raws0"]["run1"]
          raw2 = self["raws0"]["run2"]
          raw3 = self["raws0"]["run3"]
          raw4 = self["raws0"]["run4"]


          events[:33]
          event_id
          self.meta["events"][key0]

          self.info(2)

          str(self["epochs0"]["run0"]["data"]).split("\n")[:22]

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        epochs0_list = list()
        runs = self.meta["run_increments"]
        for key0,raw0 in self[raws0].items():
            self.logger.info(indS(1)+"RUN: {}.{}(...)".format(self.stack,"CUSTOM_CODE"))
            self.logger.info(indS(1)+"NOW: {}".format(key0))

            events, event_id = mne.events_from_annotations(raw0)
            events = events[ (100<events[:,2]) & (events[:,2]<241) ]
            events[:,2] = events[:,2] + runs[key0]
            EVENT_ID = dc(self.meta["events"][key0])

            if export:
                od_path = self.locs.od_path/"export_epochs_data"
                od_path.mkdir(mode=0o700,parents=True,exist_ok=True)
                np.savetxt(od_path/"{}.events.tsv".format(key0),events,fmt="%i %i %i")
                with open(od_path/"{}.event_id.json".format(key0),"w") as fh0:
                    json.dump(event_id,fh0,indent=4)
                    fh0.write("\n")

                with open(od_path/"{}.EVENT_ID.json".format(key0),"w") as fh0:
                    json.dump(EVENT_ID,fh0,indent=4)
                    fh0.write("\n")

            self.logger.info(indS(1)+"RUN: {}(...)".format(self.stack,"mne.Epochs"))
            picks = mne.pick_types(raw0.info,meg=False,eeg=True,exclude=[])
            ARGS = dict(
                raw      = raw0.copy(),
                events   = events,
                event_id = EVENT_ID,
                metadata = None,
                tmin     = tmin,
                tmax     = tmax,
                baseline = baseline,
                picks    = picks,
                preload  = False, ## TODO FIXME CHECK IT OUT
                reject_by_annotation = True,
                reject   = None, # use autoreject later on
                flat     = None, # use autoreject later on
                decim    = 1,
            )
            for line in str_dict(ARGS,indD(1)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.debug(line)
            epochs0_item = mne.Epochs(**ARGS).load_data().resample(
                sfreq   = self.meta["resamp"]["sfreq"],
                npad    = "auto",
                window  = "boxcar",
                n_jobs  = 1,
                pad     = "edge",
                verbose = None,
            )
            epochs0_list.append(epochs0_item.copy())
            if export:
                # TODO SUBM a BUG report to MNE
                # epochs0_item.save() has problem with unicode/utf-8
                # it tries to use latin-1
                hkl.dump(
                    epochs0_item,
                    od_path/"{}-epo.fif.hkl.gz".format(key0),
                    mode="w",
                    compression="gzip",
                )

        self.logger.info(indS(1)+"RUN: {}(...)".format(self.stack,"mne.concatenate_epochs"))
        epochs0_cat = mne.concatenate_epochs(epochs0_list)
        self[epochs0] = OrderedDict()
        self[epochs0]["data"] = epochs0_cat.copy()
        if export:
            key0 = "run0"
            hkl.dump(
                epochs0_cat,
                od_path/"{}.-epo.fif.hkl.gz".format(key0),
                mode="w",
                compression="gzip",
            )
            np.savetxt(od_path/"{}.events.tsv".format(key0),epochs0_cat.events,fmt="%i %i %i")
            with open(od_path/"{}.EVENT_ID.json".format(key0),"w") as fh0:
                json.dump(epochs0_cat.event_id,fh0,indent=4)
                fh0.write("\n")


    def construct_evoked(
            self,
            epochs0,
            comment = True,
            conds   = ["word","verb","noun","noun/F","noun/M","len7","len8","len9"],
    ):
        """
        Example use:
          self.construct_evoked(
            epochs0 = "epochs0",
            comment = True,
            conds   = ["word","verb","noun","noun/F","noun/M","len7","len8","len9"],
          )
          self.info(3)

        Testing:
          epochs0 = "epochs0"
          comment = True

          self[epochs0]["evokeds"]["noun"].comment
          self[epochs0]["evokeds"]["noun"].nave

          conds0 = [
              "word",
              "verb",
              "noun",
              "noun/F",
              "noun/M",
              "len7",
              "len8",
              "len9",
              # "run1/verb",
              # "run1/noun",
              # "run4/verb",
              # "run4/noun",
              # ["run3/noun","run4/noun"],
          ]

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        epochs0_reref = self[epochs0]["data"] \
                      .copy() \
                      .apply_baseline(baseline=(None,0)) \
                      .set_eeg_reference(
                          ref_channels = self.meta["ref"]["rref"],
                          projection   = False,
                          ch_type      = "eeg",
                      )

        self[epochs0]["evokeds"] = OrderedDict()
        for cond in conds:
            key0 = str(cond).replace("/","_").strip("[").strip("]").strip("'").replace("', '","_OR_")
            self[epochs0]["evokeds"][key0] = epochs0_reref[cond].average()
            if comment: self[epochs0]["evokeds"][key0].comment = key0


    def extract_evoked_features(
            self,
            epochs0,
            tool0,
            mode0,
            spans0,
            chans0,
            bunds0,
            plots0 = False,
    ):
        """
        Example use:
          self.extract_evoked_features(
            epochs0 = "epochs0",
            tool0   = "mne",
            mode0   = "neg",
            spans0  = self.meta["time"]["spans0"],
            chans0  = None, # self.meta["bund"]["base3"]["B1"],
            bunds0  = self.meta["bund"]["base0"],
          )
          self.info(2)

        Testing:
          epochs0 = "epochs0"
          tool0   = "mne"
          mode0   = "neg"
          spans0  = self.meta["time"]["spans0"]

          chans0  = self.meta["bund"]["base3"]["B1"]
          bunds0  = None

          chans0  = None
          bunds0  = self.meta["bund"]["base0"]

          plots0  = True

        Testing a single iteration (with PLOTS)
          plt.close("all")

          tool0 = "mne"
          tool0 = "sci"
          tool0 = "raw"

          mode0 = "pos"
          mode0 = "neg"
          mode0 = "abs"
          mode0 = "min"
          mode0 = "max"
          mode0 = "avg"
          mode0 = "std"
          mode0 = "mix"
          mode0 = "sad"
          mode0 = "tpz"

          K = ["2","3"]
          K = ["2"]
          spans0 = self.meta["time"]["spans0"]
          spans0 = {k: spans0.get(k, None) for k in K}

          bunds0 = None
          K = np.array([0,4,6])
          K = np.array([4])
          chans0  = self.meta["bund"]["base3"]["B1"]
          chans0 = list(np.array(chans0)[K.astype(int)])

          chans0 = None
          K = ["FR","PL"]
          K = ["PL"]
          bunds0 = self.meta["bund"]["base0"]
          bunds0 = {k: bunds0.get(k, None) for k in K}

          K = ["verb"]
          K = ["noun","verb"]
          cond0 = self["epochs0"]["evokeds"]
          cond0 = {k: cond0.get(k, None) for k in K}
          self["epochs0_TEST"] = OrderedDict()
          self["epochs0_TEST"]["evokeds"] = cond0

          self.extract_evoked_features(
            epochs0 = "epochs0_TEST",
            tool0   = tool0,
            mode0   = mode0,
            spans0  = spans0,
            chans0  = chans0,
            bunds0  = bunds0,
            plots0  = True,
          )

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        from._valid import valid_feats0

        assert tool0 in list(valid_feats0.keys()),"PROBLEM: got tool0={} but it should be one of {})".format(repr(tool0),list(valid_feats0.keys()))
        assert mode0 in valid_feats0[tool0],"PROBLEM: got mode0={} but for tool0={} mode0 should be one of {}".format(repr(mode0),repr(tool0),valid_feats0[tool0])
        assert (chans0 is None)^(bunds0 is None),"PROBLEM: please provide EITHER chans0 OR bunds0 (the other of the two should be None)"
        type0  = "bunds0" if (bunds0 is not None) else "chans0"

        subj0  = self.sub
        # sess0  = self.ses
        # task0  = self.task
        runn0  = int(self.run)
        later0 = np.nan
        front0 = np.nan
        clust0 = np.nan

        self.logger.debug(indD(1)+"type0: {}".format( type0 ))
        self.logger.debug(indD(1)+"subj0: {}".format( subj0 ))
        self.logger.debug(indD(1)+"runn0: {}".format( runn0 ))

        # Add sub-keys to self[epochs0] if required
        if "feats" not in self[epochs0].keys():                  self[epochs0]["feats"] = OrderedDict()
        if tool0  not in self[epochs0]["feats"].keys():         self[epochs0]["feats"][tool0] = OrderedDict()
        if mode0   not in self[epochs0]["feats"][tool0].keys(): self[epochs0]["feats"][tool0][mode0] = OrderedDict()
        self[epochs0]["feats"][tool0][mode0][type0] = None
        """
        self.info(4)

        """
        df0 = pd.DataFrame(
            data=[],
            columns=[
                "epochs0", # method argument
                "tool0",   # method argument
                "mode0",   # method argument
                "type0",   # "bunds0" OR "chans0" inferred from bunds0 and chans0 arguments
                "cond0",   # iterate over all that are present in self[epochs0]["evokeds"]
                "chan0",   # EEG channel (physical or a bundle made by averaging physical channels)
                "later0",  # from self.meta based on "chan0"
                "front0",  # from self.meta based on "chan0"
                "clust0",  # from self.meta based on "chan0" (np.nan for real bundles)
                "tmin0",   # from timespans0 argument (iterated over)
                "tmax0",   # from timespans0 argument (iterated over)
                "subj0",   # from self.sub
                "goodZ",   #
                "goodJ",   #
                "runn0",   # TODO: FUTURAMA: consider extracting run number as factor from condition code
                "nave0",   # from self[epochs0]["evokeds"][cond0] (iterated over)
                "chanX",
                "latX",
                "valX",
            ],
        )
        EVOKEDS = dc(self[epochs0]["evokeds"])
        for idx0,(cond0,data0) in enumerate(EVOKEDS.items()):
            """
            idx0 = 0
            cond0 = "verb"
            data0 = EVOKEDS[cond0]
            data0

            """
            nave0 = data0.nave
            self.logger.debug(indD(1)+"idx0={}; cond0={} ({})".format(idx0,repr(str(cond0)),nave0))
            if bunds0 is not None:
                self.logger.debug(indD(1)+"combining channels in bundles")
                ch_names  = data0.info["ch_names"]
                bunds0idx = OrderedDict()
                for key0,val0 in bunds0.items():
                    bunds0idx[key0] = mne.pick_channels(ch_names, val0 )

                """
                data1
                bunds0idx
                print(np.array(data0.info["ch_names"])[bunds0idx["PL"].astype(int)])
                print(self.meta["bund"]["base0"]["PL"])

                """
                data1 = mne.channels.combine_channels(
                    inst   = dc(data0),
                    groups = bunds0idx,
                    method = "mean",
                )
            else:
                self.logger.debug(indD(1)+"working on channels data")
                data1 = dc(data0).pick(chans0)

            for chan0 in data1.ch_names:
                """
                chan0 = data1.ch_names[4]
                chan0

                """
                self.logger.debug(indD(2)+"chan0: {}".format(repr(str( chan0 ))))
                for span0 in list(spans0.values()):
                    """
                    span0 = list(spans0.values())[0]
                    span0 = list(spans0.values())[1]
                    span0

                    """
                    self.logger.debug(indD(2)+"span0: {}".format(repr(str( span0 ))))
                    tmin0 = span0[0]
                    tmax0 = span0[1]
                    smin0,smax0 = data1.time_as_index([tmin0,tmax0])
                    self.BATCH.logger.debug(indD(2)+"tmin0: {}".format( tmin0 ))
                    self.BATCH.logger.debug(indD(2)+"tmax0: {}".format( tmax0 ))
                    self.BATCH.logger.debug(indD(2)+"smin0: {}".format( smin0 ))
                    self.BATCH.logger.debug(indD(2)+"smax0: {}".format( smax0 ))
                    data2 = data1.copy().pick(chan0).crop(tmin=tmin0,tmax=tmax0)
                    assert data2.data.shape[0] == 1,"PROBLEM: For peak detection EXACTLY ONE channel was expected, got {}".format(data2.data.shape[0])
                    data2_arr  = data2.copy().data[0,:]
                    if plots0:
                        fig0 = data0.plot()
                        fig1 = data1.plot()
                        fig2 = data2.plot()
                        fig0.axes[0].plot( data1.times[smin0:smax0+1],data2_arr*1e6,c="red",linestyle="dotted", )
                        fig1.axes[0].plot( data1.times[smin0:smax0+1],data2_arr*1e6,c="red",linestyle="dotted", )

                    if   tool0 == "mne":
                        """
                        print( tmin0 )
                        print( tmax0 )
                        print( mode0 )

                        """
                        try:
                            chanX,latX,valX = data2.copy().get_peak(
                                ch_type          = "eeg",
                                tmin             = tmin0,
                                tmax             = tmax0,
                                mode             = mode0,
                                return_amplitude = True,
                            )
                        except ValueError:
                            self.logger.warning(indD(0)+"*** WARNING *** handling ValueError for {}".format(repr(str( chan0 ))))
                            chanX,latX,valX = chan0,np.nan,np.nan

                    elif tool0 == "sci":
                        if mode0 == "neg": data2_arr *= -1
                        sampX,_ = find_peaks(
                            x            = data2_arr,
                            height       = None,
                            threshold    = None,
                            distance     = 4e4,
                            prominence   = None,
                            width        = None,
                            wlen         = None,
                            rel_height   = 0.5,
                            plateau_size = None,
                        )
                        chanX = chan0
                        valX  = data2_arr[sampX]
                        latX  = data2.times[sampX] # data1.times[sampX+smin0]
                        latX  = latX[0] if latX.size > 0 else np.nan
                        valX  = valX[0] if valX.size > 0 else np.nan
                        if mode0 == "neg": data2_arr *= -1
                        if mode0 == "neg": valX *= -1

                    elif tool0 == "raw":
                        chanX = chan0
                        if mode0 == "min":
                            sampX = np.argmin(data2_arr)
                            valX  = data2_arr[sampX]
                            latX  = data2.times[sampX]

                        if mode0 == "max":
                            sampX = np.argmax(data2_arr)
                            valX  = data2_arr[sampX]
                            latX  = data2.times[sampX]

                        if mode0 == "avg":
                            valX  = data2_arr.mean()
                            latX  = np.mean(span0)

                        if mode0 == "std":
                            valX  = data2_arr.std()
                            latX  = np.mean(span0)

                        if mode0 == "mix":
                            valX  = np.amax( data2_arr ) - np.amin( data2_arr )
                            latX  = np.mean(span0)

                        if mode0 == "sad":
                            valX  = np.abs( np.diff( data2_arr ) ).sum()
                            latX  = np.mean(span0)

                        if mode0 == "tpz":
                            valX  = np.trapz( data2_arr )
                            latX  = np.mean(span0)

                    else:
                        raise NotImplementedError

                    if plots0:
                        fig1.axes[0].plot( latX, valX*1e6, "X", color="#0000cc" if mode0=="neg" else "#cc0000", markersize=12, alpha=.5, )
                        fig2.axes[0].plot( latX, valX*1e6, "X", color="#0000cc" if mode0=="neg" else "#cc0000", markersize=12, alpha=.5, )
                        fig0.axes[0].plot( latX, valX*1e6, "X", color="#0000cc" if mode0=="neg" else "#cc0000", markersize=12, alpha=.5, )

                    valX *= 1e6
                    df1 = pd.DataFrame(
                        data=[[
                            epochs0, # method argument
                            tool0,   # method argument
                            mode0,   # method argument
                            type0,   # "bunds0" OR "chans0" inferred from bunds0 and chans0 arguments
                            cond0,   # iterate over all that are present in self[epochs0]["evokeds"]
                            chan0,   # EEG channel (physical or a bundle made by averaging physical channels)
                            later0,  # [TODO] from self.meta based on "chan0"
                            front0,  # [TODO] from self.meta based on "chan0"
                            clust0,  # [TODO] from self.meta based on "chan0" (np.nan for real bundles)
                            tmin0,   # from timespans0 argument (iterated over)
                            tmax0,   # from timespans0 argument (iterated over)
                            subj0,   # from self.sub
                            np.nan,  # PLACEHOLDER for goodZ
                            np.nan,  # PLACEHOLDER for goodJ
                            runn0,   # TODO: FUTURAMA: consider extracting run number as factor from condition code
                            nave0,   # from self[epochs0]["evokeds"][cond0] (iterated over)
                            chanX,
                            latX,
                            valX,
                        ]],
                        columns=df0.columns,
                    )
                    df0 = df0.append(df1)

        ## Map missing details
        df0["later0"] = df0["chan0"].map(self.meta["bund"]["base5"]["later0"] )
        df0["front0"] = df0["chan0"].map(self.meta["bund"]["base5"]["front0"] )
        df0["clust0"] = df0["chan0"].map(self.meta["bund"]["base5"]["clust0"] )
        df0["goodZ"]  = df0["subj0"].map(self.incl["good"]["z0"] )
        df0["goodJ"]  = df0["subj0"].map(self.incl["good"]["j0"] )

        ## Insert dataframe
        self[epochs0]["feats"][tool0][mode0][type0] = dc(df0)


    def extract_evoked_features_in_bulk(
            self,
            epochs0,
            spans0,
            chans0,
            bunds0,
            feats0 = None,
    ):
        """
        Example:
          extract_evoked_features_in_bulk(
            epochs0 = "epochs0",
            spans0  = self.meta["time"]["spans0"],
            chans0  = self.meta["bund"]["base3"]["B1"],
            bunds0  = self.meta["bund"]["base0"],
            feats0  = self.meta["feat"]["valid0"],
          )
          self.info(4)

        Testing:

          K = ["2"]
          K = ["2","3"]
          spans0 = self.meta["time"]["spans0"]
          spans0 = {k: spans0.get(k, None) for k in K}

          K = np.array([4])
          K = np.array([0,4,6])
          chans0  = self.meta["bund"]["base3"]["B1"]
          chans0 = list(np.array(chans0)[K.astype(int)])

          K = ["PL"]
          K = ["FR","PL"]
          bunds0 = self.meta["bund"]["base0"]
          bunds0 = {k: bunds0.get(k, None) for k in K}

          K = ["verb"]
          K = ["noun","verb"]
          cond0 = self["epochs0"]["evokeds"]
          cond0 = {k: cond0.get(k, None) for k in K}
          self["epochs0_TEST"] = OrderedDict()
          self["epochs0_TEST"]["evokeds"] = cond0

          self.extract_evoked_features_in_bulk(
            epochs0 = "epochs0_TEST",
            spans0  = spans0,
            chans0  = chans0,
            bunds0  = bunds0,
            feats0  = self.meta["feat"]["valid0"],
          )


        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        from._valid import valid_feats0

        if feats0 is None:
            try:
                feats0  = self.meta["feat"]["valid0"]
            except KeyError:
                feats0 = valid_feats0

        for tool0,modes0 in feats0.items():
            assert tool0 in list(valid_feats0.keys()),"PROBLEM: got tool0={} but it should be one of {})".format(repr(tool0),list(valid_feats0.keys()))
            for mode0 in modes0:
                assert mode0 in valid_feats0[tool0],"PROBLEM: got mode0={} but for tool0={} mode0 should be one of {}".format(repr(mode0),repr(tool0),valid_feats0[tool0])

        time0_t0 = time.time()

        for tool0,modes0 in feats0.items():
            for mode0 in modes0:
                if chans0 is not None:
                    self.extract_evoked_features(
                        epochs0 = epochs0,
                        tool0   = tool0,
                        mode0   = mode0,
                        spans0  = spans0,
                        chans0  = chans0,
                        bunds0  = None,
                    )

                if bunds0 is not None:
                    self.extract_evoked_features(
                        epochs0 = epochs0,
                        tool0   = tool0,
                        mode0   = mode0,
                        spans0  = spans0,
                        chans0  = None,
                        bunds0  = bunds0,
                    )

        time0_t1 = time.time()
        time0_d1 = time0_t1-time0_t0
        self.logger.info(indS(0)+("="*77))
        self.logger.info(indS(0)+("="*77))
        self.logger.info(indS(0)+"DONE: {}".format(self.sub))
        self.logger.info(indS(0)+"TIME: {}".format(hf.format_timespan(time0_d1)))
        self.logger.info(indS(0)+("="*77))
        self.logger.info(indS(0)+("="*77))


    def merge_evoked_features(
            self,
            epochs0,
    ):
        """

        Testing:
          self.merge_evoked_features(
            epochs0 = "epochs0",
          )

        Testing:
          epochs0 = "epochs0"

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        # Get the first dataframe
        temp0 = self[epochs0]["feats"]
        while isinstance(temp0,dict):
            temp0 = next(iter(temp0.values()))

        df0 = pd.DataFrame([],columns=temp0.columns)
        # self[epochs0]["feats"][tool0][mode0][type0]
        tools0 = self[epochs0]["feats"]
        for tool0,modes0 in tools0.items():
            for mode0,types0 in modes0.items():
                for type0,df1 in types0.items():
                    self.logger.debug(indS(0)+"MERGING: {}/{}/{} [{}]".format(tool0,mode0,type0,df1.shape[0]))
                    df0 = df0.append(df1)

        self[epochs0]["FEATS"] = dc(df0)


    def write_hkl(
            self,
            suffStr   = "",
            overwrite = False,
    ):
        """
        Example:
          self.write_hkl(
            suffStr   = "",
            overwrite = False,
          )

        Testing:
          self.write_hkl("TEST",False)
          self.write_hkl("TEST",False)
          self.write_hkl("TEST",True)
          self.write_hkl("test2",True)

          test = hkl.load(fileobj = "outputs/st.0101/sub-18skxm/ses-eeg001/eeg/sub-18skxm_ses-eeg001_task-lexdec_run-000_eeg.TEST.gzip.hkl")

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        of_extn = "gzip.hkl" # "gzip.hkl" | "hkl.gz"
        of_suff = ""
        of_suff = ".".join([of_suff,suffStr] if suffStr else [of_suff])
        of_suff = ".".join([of_suff,of_extn])
        of_name = self.locs.of_base.with_suffix(of_suff)
        if overwrite or (not os.path.exists(of_name)):
            hkl.dump(
                self.data,
                of_name,
                mode="w",
                compression="gzip",
            )
        else:
            self.logger.warning(indS(1)+"adding UUID to filename to avoid overwriting of the output file ")
            of_suff = ""
            of_suff = ".".join([of_suff,suffStr] if suffStr else [of_suff])
            of_suff = ".".join([of_suff,self.uuid4])
            of_suff = ".".join([of_suff,of_extn])
            of_name = self.locs.of_base.with_suffix(of_suff)
            assert overwrite or (not os.path.exists(of_name)), "PROBLEM: tried NOT to overwrite HKL output (as perscribed) but failed badly because the target file (uuid4) exists"
            hkl.dump(
                self.data,
                of_name,
                mode="w",
                compression="gzip",
            )

        self.logger.info (indS(1)+"saved: {}".format(repr(str(of_name))))


    def read_hkl(
            self,
            fileobj = None,
    ):
        """

        Example:
          self.read_hkl()
          self.read_hkl(fileobj=None)

        Testing:
          self.read_hkl(fileobj="TEST.hkl.gz")
          self.read_hkl("outputs/st.0101/sub-18skxm/ses-eeg001/eeg/sub-18skxm_ses-eeg001_task-lexdec_run-000_eeg.test2.hkl.gz")

          test = hkl.load(fileobj = "outputs/st.0101/sub-18skxm/ses-eeg001/eeg/sub-18skxm_ses-eeg001_task-lexdec_run-000_eeg.TEST.gzip.hkl")

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        if fileobj is None:
            fileobj = self.locs.if_path

        self.data = hkl.load(fileobj=fileobj)
        self.logger.info(indS(1)+"{} was loaded".format(str(fileobj)))


    def plot_epochs_drop_log(
            self,
            epochs0,
            showFig,
            saveFig,
            suffStr = "",
    ):
        """
        Example:
          self.plot_epochs_drop_log(
            epochs0 = "epochs1",
            showFig = _SHOW_FIGS,
            saveFig = _SAVE_FIGS,
            suffStr   = "fix201",
          )

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        fig = self[epochs0]["data"]\
                  .plot_drop_log(show=False)
        fig.set_size_inches(16,8)

        title_old = fig.axes[0].get_title()
        title_new = "{}\n{} {} (keep: {}, drop: {})".format(
            str(self.locs.of_stem),
            epochs0,
            title_old,
            len(self[epochs0]["data"]),
            len([item for item in self[epochs0]["data"].drop_log if len(item) != 0]),
        )
        fig.axes[0].set(title=title_new)
        if showFig: (fig or plt).show()
        if saveFig:
            od_path = self.locs.od_path/"export_figs"
            od_path.mkdir(mode=0o700,parents=True,exist_ok=True)
            of_suff = ""
            of_suff = ".".join([of_suff,str(whoami())])
            of_suff = ".".join([of_suff,epochs0])
            of_suff = ".".join([of_suff,suffStr] if suffStr else [of_suff])
            of_suff = ".".join([of_suff,"png"])
            of_name = (od_path/self.locs.of_stem).with_suffix(of_suff)
            self.logger.debug(indD(1)+"of_name: {}".format(repr(str(of_name))))
            fig.savefig(of_name, dpi=fig.dpi,)


    def plot_autorejection_log(
            self,
            epochs0,
            epochs1,
            showFig,
            saveFig,
            suffStr = "",
            rLogKey = "rLog",
    ):
        """
        Example:
          self.plot_autorejection_log(
            epochs0 = "epochs0", # DIRTY, DIRTY, ROTTEN EPOCHS!!!
            epochs1 = "epochs2", # CLEAN EPOCHS!!!
            showFig = _SHOW_FIGS,
            saveFig = _SAVE_FIGS,
            suffStr = "fix201",
          )

        Testing:
            epochs0 = "epochs0" # DIRTY, DIRTY, ROTTEN EPOCHS!!!
            epochs1 = "epochs2" # CLEAN EPOCHS!!!
            showFig = _SHOW_FIGS
            saveFig = _SAVE_FIGS
            suffStr = "TEST.fix201"
            rLogKey = "rLog"


        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        epochs_dirty = self[epochs0]["data"]
        reject_log   = self[epochs1][rLogKey]

        ch_names = epochs_dirty.info["ch_names"]
        fig = reject_log.plot(
            orientation = "horizontal",
            show        = False,
        )
        fig.subplots_adjust(top=0.9)
        fig.axes[0].set_xticks(range(len(epochs_dirty)))
        fig.axes[0].set_yticks(range(len(ch_names    )))
        fig.axes[0].set_xticklabels(range(len(epochs_dirty)))
        fig.axes[0].set_yticklabels(["{} [{}]".format(chan0,num0) for num0,chan0 in enumerate(ch_names)])
        fig.axes[0].set_xticks(np.arange(-.5, len(epochs_dirty), 1), minor=True);
        fig.axes[0].set_yticks(np.arange(-.5, len(ch_names)    , 1), minor=True);
        fig.axes[0].grid(which="minor", color="k", linestyle="-", linewidth=1)
        fig.axes[0].tick_params(axis="both", which="major", labelsize=6)
        fig.axes[0].tick_params(axis="both", which="minor", labelsize=6)
        fig.axes[0].images[0].set_cmap( plt.get_cmap("YlOrRd", 3) )
        fig.axes[0].grid(b=False, which="major", axis="both",)
        fig.axes[0].grid(b=True,  which="minor", axis="both",)
        labels0 = fig.axes[0].get_xticklabels()
        for label0 in labels0:
            label0.set_rotation(90)

        cbar = plt.colorbar(
            fig.axes[0].images[-1],
            ax=fig.axes[0],
            shrink=.3,
            label="Problem",
            ticks=[0,1,2],
        )
        cbar.ax.set_yticklabels(['GOOD','BAD','Interpolated (was BAD, now is GOOD)'])

        fig.set_size_inches(28,8)

        title_old = fig.axes[0].get_title()
        title_new = "{}\n{} {} (keep: {}, drop: {})".format(
            str(self.locs.of_stem),
            epochs1,
            rLogKey,
            len(self[epochs1]["data"]),
            len([item for item in self[epochs1]["data"].drop_log if len(item) != 0]),
        )
        fig.axes[0].set(title=title_new)
        plt.tight_layout()
        if showFig: (fig or plt).show()
        if saveFig:
            od_path = self.locs.od_path/"export_figs"
            od_path.mkdir(mode=0o700,parents=True,exist_ok=True)
            of_suff = ""
            of_suff = ".".join([of_suff,str(whoami())])
            of_suff = ".".join([of_suff,epochs1])
            of_suff = ".".join([of_suff,rLogKey])
            of_suff = ".".join([of_suff,suffStr] if suffStr else [of_suff])
            of_suff = ".".join([of_suff,"png"])
            of_name = (od_path/self.locs.of_stem).with_suffix(of_suff)
            self.logger.debug(indD(1)+"of_name: {}".format(repr(str(of_name))))
            fig.dpi = 300
            fig.savefig(of_name, dpi=fig.dpi,)






    def run_ica(
            self,
            epochs0,
            n_components = 0.98,
            random_state = 0,
            icaKey       = "ica0",
    ):
        """
        Example:
          self.run_ica(
            epochs0      = "epochs2",
            n_components = 0.98,
            random_state = 0,
            icaKey       = "ica0",
          )

        Testing:
            epochs0      = "epochs2"
            n_components = 0.98
            random_state = 0
            icaKey       = "ica0"

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        ARGS = dict(
            n_components       = n_components,
            # n_components       = 50,
            # n_pca_components   = 50,
            # max_pca_components = 50,
            # method             = "fastica",
            method             = "infomax",
            fit_params         = dict(extended=True),
            max_iter           = 6400,
            # noise_cov          = noise_cov,
            random_state       = random_state,
        )
        for line in str_dict(ARGS,indD(1)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)
        time_t0 = time.time()
        self[epochs0][icaKey] = mne.preprocessing.ica.ICA(
            **ARGS
        ).fit(
            self[epochs0]["data"],
        )
        time_t1 = time.time()
        time_d1 = time_t1-time_t0
        self.logger.info(indD(1)+"time elapsed: {}".format(hf.format_timespan(time_d1)))


    def inspect_components(
            self,
            epochs0,
            showFig,
            saveFig,
            suffStr = "",
            icaKey  = "ica0",
    ):
        """
        Example:
          self.inspect_components(
            epochs0 = "epochs2",
            showFig = _SHOW_FIGS,
            saveFig = _SAVE_FIGS,
            suffStr = "fix201",
            icaKey  = "ica0",
          )

        Testing:
            epochs0 = "epochs2"
            showFig = _SHOW_FIGS
            saveFig = _SAVE_FIGS
            suffStr = "fix201"
            icaKey  = "ica0"

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        title = "ICA Componentts\n"
        title += str(self.locs.of_stem)
        # TODO FIXME This can also output a single figure object
        # (not necesarily a list of figs)
        figs = self[epochs0][icaKey].plot_components(
            inst   = self[epochs0]["data"],
            title  = title,
            show   = False,
        )
        for ii,fig in enumerate(figs):
            fig.set_size_inches(16,16)
            if showFig: (fig or plt).show()
            if saveFig:
                od_path = self.locs.od_path/"export_figs"
                od_path.mkdir(mode=0o700,parents=True,exist_ok=True)
                of_suff = ""
                of_suff = ".".join([of_suff,str(whoami())])
                of_suff = ".".join([of_suff,epochs0])
                of_suff = ".".join([of_suff,icaKey])
                of_suff = ".".join([of_suff,suffStr] if suffStr else [of_suff])
                of_suff = ".".join([of_suff,"{:03d}".format(ii)])
                of_suff = ".".join([of_suff,"png"])
                of_name = (od_path/self.locs.of_stem).with_suffix(of_suff)
                self.logger.debug(indD(1)+"of_name: {}".format(repr(str(of_name))))
                fig.dpi = 300
                fig.savefig(of_name, dpi=fig.dpi,)


    def plot_component_properties(
            self,
            epochs0,
            showFig,
            saveFig,
            suffStr  = "",
            icaKey   = "ica0",
            rejected = True,
    ):
        """
        Example:
          if sys.stdout.isatty(): plt.close("all")

          self.plot_component_properties(
            epochs0 = "epochs2",
            showFig = _SHOW_FIGS,
            saveFig = _SAVE_FIGS,
            suffStr = "fix201",
            icaKey  = "ica0",
          )

        Testing:
            epochs0 = "epochs2"
            showFig = _SHOW_FIGS
            saveFig = _SAVE_FIGS
            suffStr = "fix201"
            icaKey  = "ica0"
            rejected = True

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        exclude = sorted(self[epochs0][icaKey].exclude)
        # include = [item for item in list(range(self[epochs0][icaKey].n_components_)) if not item in exclude]
        # picks = exclude + include
        # picks = exclude if rejected else include
        # picks = None
        picks = list(range(self[epochs0][icaKey].n_components_))


        ## TODO FIXME add some logic here (or try+catch)
        ## for more elegant solution to dir handling
        # od_name = self.locs.od_path/"ICs"
        od_base = self.locs.od_path/"export_figs"/"ICs"
        od_suff = ""
        od_suff = ".".join([od_suff,epochs0])
        od_suff = ".".join([od_suff,icaKey])
        od_suff = ".".join([od_suff,suffStr] if suffStr else [od_suff])
        # od_path = self.locs.of_base.with_suffix(od_suff)
        od_path = od_base.with_suffix(od_suff)
        od_path.mkdir(mode=0o700,parents=True,exist_ok=True)
        shutil.rmtree(od_path)
        od_path.mkdir(mode=0o700,parents=True,exist_ok=True)
        if picks:
            figs = self[epochs0][icaKey].plot_properties(
                inst  = self[epochs0]["data"],
                picks = picks,
                show  = False,
            )
            for ii,fig in enumerate(figs):
                STATUS = "EXC" if (ii in exclude) else "INC"
                fig.set_size_inches(16,16)
                title_old = fig.axes[0].get_title()
                title_new = "{}\n{} {} {} [{:03d}] {}".format(
                    str(self.locs.of_stem),
                    epochs0,
                    icaKey,
                    title_old,
                    ii,
                    STATUS,
                )
                fig.axes[0].set(title=title_new)
                if showFig: (fig or plt).show()
                if saveFig:
                    of_name = str(self.locs.of_stem)
                    # of_name = ".".join([of_name,str(whoami())])
                    of_name = ".".join([of_name,epochs0])
                    of_name = ".".join([of_name,icaKey])
                    of_name = ".".join([of_name,STATUS])
                    of_name = ".".join([of_name,"{:03d}".format(ii)])
                    of_name = ".".join([of_name,suffStr] if suffStr else [of_name])
                    of_name = ".".join([of_name,"png"])
                    ## CAUTION: using a subdir here
                    of_path = od_path/of_name
                    self.logger.info(indD(1)+"of_path: {}".format(repr(str( of_path ))))
                    fig.dpi = 300
                    fig.savefig(of_path, dpi=fig.dpi,)


    def export_components(
            self,
            epochs0,
            excKey,
            suffStr   = "",
            overwrite = False,
    ):
        """
        Example:
          self.export_components(
            epochs0   = "epochs2",
            excKey    = "exc0",
            suffStr   = "fix201.AUTO",
            overwrite = False,
          )

        Testing:
            epochs0   = "epochs2"
            excKey    = "exc0"
            suffStr   = "fix201.test"
            overwrite = False

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        of_suff = ""
        # of_suff = ".".join([of_suff,str(whoami())])
        of_suff = ".".join([of_suff,epochs0])
        of_suff = ".".join([of_suff,excKey])
        of_suff = ".".join([of_suff,suffStr] if suffStr else [of_suff])
        of_suff = ".".join([of_suff,"txt"])
        of_name = self.locs.of_base.with_suffix(of_suff)

        exclude = dc(self[epochs0][excKey])

        self.logger.info(indD(1)+"of_name: {}".format(repr(str( of_name ))))
        self.logger.info(indD(1)+"comps: {}"  .format(repr(str( exclude ))))
        if overwrite or (not os.path.exists(of_name)):
            self.logger.info(indD(1)+"writing BAD components informtion to file")
            with open(of_name, 'w') as fh:
                for item in exclude:
                    fh.write("{} # {} # {}\n".format(item,excKey,of_suff))

        else:
            self.logger.info(indD(1)+"file exists and overwrite option is set to False")
            self.logger.info(indD(1)+"doing nothing")

        self.logger.info(indD(1)+"DONE!")






    def import_components(
            self,
            epochs0,
            excKey,
            suffStr = "",
    ):
        """
        Example:
          self.import_components(
            epochs0   = "epochs2",
            excKey    = "exc0",
            suffStr   = "fix201.USER",
          )

        Testing:
            epochs0   = "epochs2"
            excKey    = "exc0"
            suffStr   = "fix201.USER"

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        of_suff = ""
        # of_suff = ".".join([of_suff,str(whoami())])
        of_suff = ".".join([of_suff,epochs0,excKey])
        of_suff = ".".join([of_suff,suffStr] if suffStr else [of_suff])
        of_suff = ".".join([of_suff,"txt"])
        of_name = self.locs.of_base.with_suffix(of_suff)

        bad_comps = list()
        self.logger.debug(indD(1)+"of_name: {}".format(repr(str(of_name))))
        assert os.path.exists(of_name), "PROBLEM: file {} not found".format(repr(str(of_name)))
        with open(of_name) as fh:
            for line in fh:
                line = line.split('#',1,)[0].strip()
                if line:
                    bad_comps.append(int(line))

        bad_comps = sorted(list(set(bad_comps)))
        self.logger.info (indD(1)+"bad_comps: {}".format(repr(str(bad_comps))))
        return bad_comps










    def plot_evoked_comparison(
            self,
            epochs0,
            cond0s,
            chan0,
            showFig,
            saveFig,
            suffStr    = "",
            fig_size   = None,
            ylim       = None,
            combine    = None,
            colors     = None,
            styles     = None,
            linestyles = None,
            vlines     = None,
            time0s     = None,
            peaksDF    = None,
            tool0      = None,
            mode0      = None,
    ):
        """
        Example:
          if sys.stdout.isatty(): plt.close("all")

          self.plot_evoked_comparison(
            epochs0    = "epochs2",
            cond0s     = ["verb","noun","noun_M","noun_F"],
            chan0      = dict(PL=["P3","P5","P7","PO3","PO7","O1"]), # "C3"
            showFig    = _SHOW_FIGS,
            saveFig    = _SAVE_FIGS,
            suffStr    = "test251",

            fig_size   = dict(w=10,h=8),
            ylim       = dict(eeg=[-15,15]),
            combine    = "mean",
            colors     = None,
            styles     = None,
            linestyles = None,
            vlines     = None,

            time0s     = self.meta["time"]["spans0"],
            peaksDF    = True,
            tool0      = "sci",
            mode0      = "pos",
          )



        """
        self.logger.debug(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.debug(line)

        chan0_PROBLEM = "PROBLEM: chan0 should be EITHER channel name (string) OR single bungle of channels (dict-like object containing a single item)"
        assert isinstance(chan0,(str,collections.Mapping)), chan0_PROBLEM
        if isinstance(chan0,(collections.Mapping)): assert len(chan0)==1, chan0_PROBLEM

        # Default values
        if fig_size   is None: fig_size   = dict(w=8,h=4)
        if ylim       is None: ylim       = dict(eeg=[-15,15])
        if combine    is None: combine    = "mean"
        if colors     is None: colors     = dict(word="#999999",verb="#e5786d",noun="#8ac6f2",noun_F="#8ac6f2",noun_M="#8ac6f2",len9="#ff38c9",len8="#a877e4",len7="#52b6ff",)
        if styles     is None: styles     = dict(word={"linewidth":1},verb={"linewidth":3},noun={"linewidth":3},noun_F={"linewidth":2},noun_M={"linewidth":2},len9={"linewidth":3},len8={"linewidth":3},len7={"linewidth": 3},)
        if linestyles is None: linestyles = dict(word="solid",verb="solid",noun="solid",noun_F="dotted",noun_M="dashed",len9="solid",len8="solid",len7="solid",)
        if vlines     is None: vlines     = list(np.round(np.linspace(0,.8,9),3))

        # Select relevant conditions (evokeds)
        evoked0s = OrderedDict((key0,val0) for key0,val0 in self.data[epochs0]["evokeds"].items() if key0 in cond0s)
        self.logger.debug(indD(1)+"GOT evoked0s: {}".format(evoked0s.keys()))

        # Pick channels
        if isinstance(chan0,(str)): chan0,combine = {chan0:[chan0]},None
        assert isinstance(chan0,(collections.Mapping)), chan0_PROBLEM
        assert len(chan0)==1, chan0_PROBLEM
        picks0 = next(iter(chan0.values()))
        assert 0 < len(picks0), "PROBLEM: picks0 should be a non-empty list"
        self.logger.debug(indD(1)+"GOT picks0: {}".format(picks0))

        # Set figure title
        title = ""
        title = " ".join([title,"Evoked: {}".format(self.locs.of_stem)])
        title = " ".join([title,"\n({})".format(epochs0)])
        title = " ".join([title,"{}".format(chan0)]) # TODO FIXME

        # Filter plotting properties to match conitions
        colors     = {key0:val0 for key0,val0 in colors    .items() if key0 in cond0s}
        styles     = {key0:val0 for key0,val0 in styles    .items() if key0 in cond0s}
        linestyles = {key0:val0 for key0,val0 in linestyles.items() if key0 in cond0s}

        # Convert times to a list of lists
        if isinstance(time0s,(collections.Mapping)): time0s = list(time0s.values())

        if time0s is None: assert vlines not in ["tmin","tmix","tmid"], "PROBLEM: vlines is set to {} (which is based on time0s but time0s is set to None)".format(vlines)

        if vlines=="tmin": vlines = [0]+[time0[0] for time0 in time0s]
        if vlines=="tmix": vlines = [0]+[ii for subL in time0s for ii in subL]
        if vlines=="tmid": vlines = [0]+[ np.round(np.mean([time0[0],time0[1]]),3) for time0 in time0s]

        ## Typically mne.viz.plot_compare_evokeds generates a list of figures.
        ## Here we produce a list of length one (hopefully not zero)
        ## Hence below we use "figs[0]"
        figs = mne.viz.plot_compare_evokeds(
            evokeds      = evoked0s,
            picks        = picks0,
            ci           = 0.95,
            ylim         = ylim,
            invert_y     = True,
            title        = title,
            show         = False,
            combine      = combine,
            colors       = colors,
            styles       = styles,
            linestyles   = linestyles,
            vlines       = vlines,
            show_sensors = True,
        )
        fig = figs[0]
        fig.set_size_inches(**fig_size)
        labels0 = fig.axes[0].get_xticklabels()
        for label0 in labels0:
            label0.set_ha("right")
            label0.set_rotation(45)
            label0.set_fontsize(9)


        if (time0s is not None):
            cmap_str = "Set3"
            cmap_str = "Set1"
            cmap_str = "tab10"
            time0c = np.unique(matplotlib.cm.get_cmap(cmap_str,len(time0s)).colors,axis=0)
            ## convert timespans (t0,t1) to start and duration
            params0 = [ [time0[0],time0[1]-time0[0]] for time0 in time0s ]
            for ii,param0 in enumerate(params0):
                rect0 = matplotlib.patches.Rectangle(
                    [param0[0],-20],
                    param0[1],
                    40,
                    angle=0.0,
                    color=time0c[ii],
                    alpha=0.3,
                )
                fig.axes[0].add_patch(rect0)


        """

            df9 = self[epochs0]["FEATS"].copy()
            peaksDF    = df9
            peaksDF    = True
            tool0      = "sci"
            mode0      = "pos"

            self.df2[ self.df2.cond0.isin(cond0)].copy()

        """
        if (time0s is not None) & (peaksDF is not None) & (tool0 is not None) & (mode0 is not None):
            if peaksDF==True: peaksDF = self[epochs0]["FEATS"]
            df0 = peaksDF.copy()
            assert len(chan0)==1, chan0_PROBLEM
            key0 = next(iter(chan0.keys()))
            df1 = df0[
                True
                & (df0["subj0"] == self.sub)
                & (df0["epochs0"] == epochs0)
                & (df0["tool0"]   == tool0)
                & (df0["mode0"]   == mode0)
                & (df0["chanX"]   == key0)
                & (df0["tmin0"]   .isin([time0[0] for time0 in time0s]))
                & (df0["cond0"]   .isin(cond0s))
            ].copy()
            arr1 = df1[["latX","valX"]].to_numpy(copy=True,)
            facecolors0 = list(colors.values())
            facecolors0 = list(itertools.chain.from_iterable(itertools.repeat(col0, len(time0s)) for col0 in facecolors0))
            edgecolors0 = list(time0c)*len(colors) if (time0s is not None) else None
            assert len(facecolors0)==len(edgecolors0), "PROBLEM: mismatch lengths for facecolors0 and edgecolors0"
            temp_dist = 0.0 # 0.2
            fig.axes[0].scatter(arr1.T[0],arr1.T[1]+temp_dist,s=48,facecolors=facecolors0,edgecolors=edgecolors0,marker="^",zorder=1200)

        return fig
