#!/usr/bin/env ipython
# -*- coding: utf-8 -*

from ipywidgets import interactive,interactive_output
from IPython.display import display, clear_output
from ipywidgets import Dropdown,SelectMultiple
from ipywidgets import Layout,Box,VBox,HBox
from ipywidgets import Output
from ipywidgets import Button
from collections import OrderedDict
import pandas as pd
import pingouin as pg
import seaborn as sns
import matplotlib as mpt
import matplotlib.pyplot as plt

import itertools

from copy import deepcopy as dc


class EvokedComparisonGroupSummaryPlotMNE():
    def __init__(self,SDF,df0,height=4,aspect=1):
        # Essentials
        self.SDF         = SDF
        self.df0         = df0
        self.height      = height
        self.aspect      = aspect
        # Layouts
        self.drop_layout = Layout(width="auto")
        # self.butt_layout = Layout(width="auto",height="auto")
        self.vbox_layout = Layout(display="flex",flex_flow="col",align_items="stretch",width="50%")
        # Widgets
        self.subj0_wgt   = Dropdown(description="subj0"  ,layout=self.drop_layout)
        self.epochs0_wgt = Dropdown(description="epochs0",layout=self.drop_layout)
        self.tool0_wgt   = Dropdown(description="tool0"  ,layout=self.drop_layout)
        self.mode0_wgt   = Dropdown(description="mode0"  ,layout=self.drop_layout)
        self.type0_wgt   = Dropdown(description="type0"  ,layout=self.drop_layout)
        self.chan0_wgt   = Dropdown(description="chan0"  ,layout=self.drop_layout)
        self.cond0_wgt   = SelectMultiple(description="cond0",layout=self.drop_layout,rows=8)
        self.tmin0_wgt   = SelectMultiple(description="tmin0",layout=self.drop_layout,rows=8)
        # self.butt0_wgt   = Button(description="RUN!",button_style="danger",layout=self.butt_layout)
        self.output0_wgt = Output(layout={"width":"100%","min_height":"1in","border":"1px solid red"})
        # UI
        self.items0      = [self.subj0_wgt,self.epochs0_wgt,self.tool0_wgt,self.mode0_wgt,self.type0_wgt,self.chan0_wgt] # self.butt0_wgt
        self.items1      = [self.cond0_wgt,self.tmin0_wgt]
        self.box0        = VBox(children=self.items0,layout=self.vbox_layout)
        self.box1        = VBox(children=self.items1,layout=self.vbox_layout)
        self.ui0         = HBox(children=[self.box0,self.box1])
        self.ui1         = VBox(children=[self.ui0,self.output0_wgt])

        # Options and values
        temp_DataMNE_key         = next(itertools.islice(self.SDF.keys(),2,3))
        temp_DataMNE_dat         = self.SDF[temp_DataMNE_key]
        self.subj0_wgt.options   = list(self.SDF.keys())
        self.subj0_wgt.value     = temp_DataMNE_key
        self.DATA                = self.SDF[self.subj0_wgt.value]
        self.df1                 = self.df0[self.df0.subj0==self.subj0_wgt.value]

        self.epochs0_wgt.options = self.df0.epochs0.unique().tolist()
        self.epochs0_wgt.value   = self.epochs0_wgt.options[0]

        self.tool0_wgt.options   = self.df0.tool0.unique().tolist()
        self.tool0_wgt.value     = self.tool0_wgt.options[0]

        self.mode0v              = OrderedDict()
        self.mode0v["mne"]       = ["pos","neg","abs",]
        self.mode0v["sci"]       = ["pos","neg",]
        self.mode0v["raw"]       = ["min","max","avg","std","mix","sad","tpz"]
        self.mode0v["bva"]       = ["min","max","MAX"]

        self.mode0_wgt.options   = self.mode0v[self.tool0_wgt.value]
        self.mode0_wgt.value     = self.mode0_wgt.options[0]

        self.type0_wgt.options   = self.df0.type0.unique().tolist()
        self.type0_wgt.value     = "bunds0"

        self.chan0v              = OrderedDict() # TODO IGNORE this can be done in a for loop
        self.chan0v["chans0"]    = self.df0[self.df0.type0=="chans0"].chan0.unique().tolist()
        self.chan0v["bunds0"]    = self.df0[self.df0.type0=="bunds0"].chan0.unique().tolist()
        self.chan0_wgt.options   = self.chan0v[self.type0_wgt.value]
        self.chan0_wgt.value     = self.chan0_wgt.options[0]

        self.tmin0_wgt.options   = ["1","2","3","4","5","6","7","8"]
        self.tmin0_wgt.value     = ["1","2","3","5"]

        self.cond0_wgt.options   = self.df0.cond0.unique().tolist()
        self.cond0_wgt.value     = ["verb","noun_F","noun_M"]

        # Observing
        self.subj0_wgt   .observe(self.subj0_upd   ,names="value")
        self.epochs0_wgt .observe(self.epochs0_upd ,names="value")
        self.tool0_wgt   .observe(self.tool0_upd   ,names="value")
        self.mode0_wgt   .observe(self.mode0_upd   ,names="value")
        self.type0_wgt   .observe(self.type0_upd   ,names="value")
        self.chan0_wgt   .observe(self.chan0_upd   ,names="value")
        self.cond0_wgt   .observe(self.cond0_upd   ,names="value")
        self.tmin0_wgt   .observe(self.tmin0_upd   ,names="value")

        # self.subj0_upd(self,self.subj0_wgt)
        display(self.ui1)
        self.g_function()



    def subj0_upd(self,*args):
        self.DATA = self.SDF[self.subj0_wgt.value]
        self.df1  = self.df0[self.df0.subj0==self.subj0_wgt.value]
        self.g_function()

    def epochs0_upd(self,*args): self.g_function()
    def tool0_upd(self,*args):   self.mode0_wgt.options = self.mode0v[self.tool0_wgt.value]; self.g_function()
    def mode0_upd(self,*args):   self.g_function()
    def type0_upd(self,*args):   self.chan0_wgt.options = self.chan0v[self.type0_wgt.value]; self.g_function()
    def chan0_upd(self,*args):   self.g_function()
    def cond0_upd(self,*args):   self.g_function()
    def tmin0_upd(self,*args):   self.g_function()
    def g_function(self):
        subj0   = self.subj0_wgt.value
        epochs0 = self.epochs0_wgt.value
        tool0   = self.tool0_wgt.value
        mode0   = self.mode0_wgt.value
        type0   = self.type0_wgt.value
        chan0   = self.chan0_wgt.value
        cond0   = self.cond0_wgt.value
        tmin0   = self.tmin0_wgt.value
        time0s  = {key0:val0 for key0,val0 in self.SDF.meta["time"]["spans0"].items() if key0 in tmin0}
        self.df2 = self.df1[
            (self.df0.subj0     == subj0  )
            & (self.df0.epochs0 == epochs0)
            & (self.df0.tool0   == tool0  )
            & (self.df0.mode0   == mode0  )
            & (self.df0.type0   == type0  )
            & (self.df0.chan0   == chan0  )
            & (self.df0.cond0   .isin(cond0)  )
            & (self.df0.tmin0   .isin([time0[0] for time0 in time0s.values()]))
        ].copy()
        if chan0 in ["FL","CL","PL","FR","CR","PR"]: chan0 = {chan0:self.DATA.meta["bund"]["base0"][chan0]}
        with self.output0_wgt:
            clear_output()
            display(self.df2.shape)
            if not self.df2.empty:
                fig = self.DATA.plot_evoked_comparison(
                    epochs0    = epochs0,
                    cond0s     = cond0,
                    chan0      = chan0,
                    showFig    = True,
                    saveFig    = False,
                    suffStr    = "test251",

                    fig_size   = dict(w=self.height*self.aspect,h=self.height),
                    ylim       = dict(eeg=[-15,15]),
                    combine    = "mean",
                    colors     = None,
                    styles     = None,
                    linestyles = None,
                    vlines     = None,

                    time0s     = time0s,
                    peaksDF    = True,
                    tool0      = tool0,
                    mode0      = mode0,
                )
                plt.show(fig)
                cols2 = ["epochs0","tool0","mode0","type0","cond0","chan0","later0","front0","clust0","tmin0","subj0","goodZ","goodJ","latX","valX"]
                display(self.df2[cols2])
