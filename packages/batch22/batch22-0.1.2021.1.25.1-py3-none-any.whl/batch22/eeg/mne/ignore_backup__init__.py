#!/usr/bin/env python
# -*- coding: utf-8 -*

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

from collections import OrderedDict
from collections import UserList
from collections import UserDict
# from dotmap import DotMap

from copy import deepcopy as dc

from deepsensemaking.bids  import get_bids_prop
from deepsensemaking.dicts import str_dict,print_dict

# DROP? import re

from ._indent import indS,indD,indN,indB
from ._whoami import whoami


import mne


class BatchMNE(UserDict):
    """MNE batch job class...
    (AKA: duct-tape + cable-ties for EEG preprocessing)
    Example usage:

      get_ipython().magic("load_ext autoreload")
      get_ipython().magic("autoreload 2")

      from collections import OrderedDict

      import batch22 as b22
      from   batch22.eeg.mne import BatchMNE
      sdf0 = BatchMNE(
        name       = "sdf0",
        metadata   = "inputs/metadata/metadata.json",
        source_ext = "vhdr",
        source_dir = "inputs/rawdata/",
        target_dir = "outputs/st.0101/",
        target_ext = "",
        done_ext   = "done",
      )
      # self = sdf0
      sdf0.get_meta()
      sdf0.get_data()

      self = sdf0["37lpxm"]

      self["test1"] = 1
      self["test2"] = 2
      self[5] = OrderedDict()
      from collections import OrderedDict
      self[5] = OrderedDict()
      self[5]["ok"] = "test"
      self.info()
      self.info(2)


    """
    def __init__(
            self,
            name       = "fds0",
            metadata   = "inputs/metadata/metadata.json",
            source_ext = "vhdr",
            source_dir = "inputs/rawdata/",
            target_dir = "outputs/st.0101/",
            target_ext = "",
            done_ext   = "done",
    ):

        ## Initialize using super-class
        UserDict.__init__(self)

        bids.config.set_option('extension_initial_dot', True)

        ## Ensure paths are of type pathlib.Path
        metadata   = pathlib.Path(metadata)
        source_dir = pathlib.Path(source_dir)
        target_dir = pathlib.Path(target_dir)

        ## Initial assertions
        assert source_dir.is_dir(),"PROBLEM: source_dir ({}) not found or not a directory".format(source_dir)
        assert metadata.is_file(),"PROBLEM: metadata file ({}) does not exist".format(metadata)
        test0 = {"name":name,"source_ext":source_ext,"done_ext":done_ext}
        for key0,val0 in test0.items():
            assert isinstance(val0,(str,)),"PROBLEM: '{}' is not a string ({})".format(key0,str(type(val0)))

        ## Initial values
        self.name       = name
        self.metadata   = metadata
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
        self.meta_meths()
        os.makedirs(self.target_dir,mode=0o700,exist_ok=True,)
        os.makedirs(self.logger_dir,mode=0o700,exist_ok=True,)
        from ._logging import setup_logger
        setup_logger(self)
        self.logger.info(indS(0)+"{} <{}> was casted, NICE!".format(self.name,type(self).__name__,))

    def keys(self):   return self.data.keys()   # TODO: check this solution against ABC and COLLECTIONS
    def vals(self):   return self.data.values() # TODO: check this solution against ABC and COLLECTIONS
    def values(self): return self.data.values() # TODO: check this solution against ABC and COLLECTIONS
    def items(self):  return self.data.items()  # TODO: check this solution against ABC and COLLECTIONS

    def __str__ (self): return str_dict(self.data,self.name,disp_types=None,tight=True)
    def __repr__(self): return str_dict(self.data,self.name,disp_types=None,tight=True)
    def _str(self):
        out_str  = ""
        out_str += indS(0)+"{} <{}>:".format(self.name,type(self).__name__,)
        out_str += indN(1)+self.name+".name       = "+repr(str( self.name       ))
        out_str += indN(1)+self.name+".metadata   = "+repr(str( self.metadata   ))
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

    def get_meta(self):
        with open(self.metadata) as fh0:
            self.meta = OrderedDict(json.load(fh0))
            self.meta_meths()

    def get_layout(self):
        self.layout = BIDSLayout(self.source_dir)

    def get_data(self):
        if self.layout is None: self.get_layout()
        if not self.meta: self.get_meta()
        subjects = self.layout.get(return_type="id",target="subject")
        for subject in subjects:
            files = self.layout.get(
                extension      = self.source_ext.lstrip("."),
                subject        = subject,
            )
            assert len(files)==4,"PROBLEM: four runs were expected for each participant"
            self[subject] = DataMNE(
                name  = subject,
                stack = self.stack,
                meta  = dc(self.meta),
                files = files,
                BATCH = self,
            )


from ._locs import LocsMNE


class DataMNE(UserDict):
    """
    self = sdf0["37lpxm"]
    """
    def __init__(self,name,stack,meta,files,BATCH):
        UserDict.__init__(self)
        self.name     = name
        self.stack    = stack+"[\"{}\"]".format(name)
        self.meta     = meta
        self.files    = files
        self.BATCH    = BATCH
        self.logger   = BATCH.logger
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
        os.makedirs(self.locs.od_path,mode=0o700,exist_ok=True,)

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
        if level is not None: out_str += indN(0)+str_dict(self.data,indD(0)+self.stack,level,tight=True)
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
        #### self[epochs0] = OrderedDict()
        for key0,raw0 in self[raws0].items():
            self.logger.info(indS(1)+"RUN: {}.{}(...)".format(self.stack,"CUSTOM_CODE"))
            self.logger.info(indS(1)+"NOW: {}".format(key0))

            events, event_id = mne.events_from_annotations(raw0)
            events = events[ (100<events[:,2]) & (events[:,2]<241) ]
            events[:,2] = events[:,2] + runs[key0]

            EVENT_ID = dc(self.meta["events"][key0])

            #### self[epochs0][key0] = OrderedDict()
            #### self[epochs0][key0]["meta"]             = OrderedDict()
            #### self[epochs0][key0]["meta"]["events"]   = events
            #### self[epochs0][key0]["meta"]["event_id"] = event_id
            #### self[epochs0][key0]["meta"]["EVENT_ID"] = EVENT_ID

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
                preload  = False, ## TODO FIXME CHECKUP THAT
                reject_by_annotation = True,
                reject   = None, # use autoreject later on
                flat     = None, # use autoreject later on
                decim    = 1,
            )
            for line in str_dict(ARGS,indD(1)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)
            #### self[epochs0][key0]["data"] = mne.Epochs(**ARGS)
            #### epochs0_list.append(self[epochs0][key0]["data"])
            epochs0_item = mne.Epochs(**ARGS).load_data().resample(
                sfreq   = self.meta["resamp"]["sfreq"],
                npad    = "auto",
                window  = "boxcar",
                n_jobs  = 1,
                pad     = "edge",
                verbose = None,
            )
            epochs0_list.append(epochs0_item.copy())

        self.logger.info(indS(1)+"RUN: {}(...)".format(self.stack,"mne.concatenate_epochs"))
        self[epochs0] = OrderedDict()
        self[epochs0]["data"] = mne.concatenate_epochs(epochs0_list)




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
          self.info(2)

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

        EPOCHS0 = self[epochs0]["data"] \
                      .copy() \
                      .apply_baseline(baseline=(None,0)) \
                      .set_eeg_reference(
                          ref_channels = self.meta["ref"]["rref"],
                          projection   = False,
                          ch_type      = "eeg",
                      )

        self[epochs0]["evokeds"] = OrderedDict()
        for cond in conds:
            key0 = str(cond).replace("/","-").strip("[").strip("]").strip("'").replace("', '","-OR-")
            self[epochs0]["evokeds"][key0] = EPOCHS0[cond].average()
            if comment: self[epochs0]["evokeds"][key0].comment = key0




    def extract_features(
            self,
            epochs0,
            class0,
            mode0,
            chans0,
            bunds0,
            timespans0,
    ):
        """
        Example use:
          self.extract_features(
            epochs0    = "epochs0",
            class0     = "mne",     # "mne" "sci" "raw"
            mode0      = "neg",     # "pos" "neg" "abs" "min" "max" "avg"
            chans0     = None, # self.meta["bund"]["base3"]["B1"],
            bunds0     = self.meta["bund"]["base0"],
            timespans0 = self.meta["time"]["spans0"],
          )
          self.info(2)

        Testing:
          epochs0    = "epochs0"
          class0     = "mne"     # "mne" "sci" "raw"
          mode0      = "neg"     # "pos" "neg" "abs" "min" "max" "avg"
          chans0     = self.meta["bund"]["base3"]["B1"]
          bunds0     = self.meta["bund"]["base0"]
          timespans0 = self.meta["time"]["spans0"]

        """
        self.logger.info(indS(0)+"RUN: {}.{}(...)".format(self.stack,whoami()))
        _args = locals(); _args.pop("self",None)
        for line in str_dict(_args,indD(0)+"args",max_level=0,max_len=42,tight=True,).split("\n"): self.logger.info(line)

        assert (chans0 is None)^(bunds0 is None),"PROBLEM: please provide EITHER chans0 or bunds0 (the other of the two should be None)"

        self[epochs0]["feats"] = None

        type0  = "bunds0" if (bunds0 is not None) else "chans0"
        subj0  = self.sub
        # sess0  = self.ses
        # task0  = self.task
        runn0  = self.run
        bund0  = np.nan
        later0 = np.nan
        coron0 = np.nan
