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


class EvokedComparisonSummaryPlotMNE():
    def __init__(self,SDF,height=4,aspect=1):
        # Essentials
        self.SDF         = SDF
        self.height      = height
        self.aspect      = aspect
        # Layouts
        self.drop_layout = Layout(width="auto")
        self.butt_layout = Layout(width="auto",height="auto")
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
        self.butt0_wgt   = Button(description="RUN!",button_style="danger",layout=self.butt_layout)
        self.output0_wgt = Output(layout={"width":"100%","min_height":"1in","border":"1px solid red"})
        # UI
        self.items0      = [self.subj0_wgt,self.epochs0_wgt,self.tool0_wgt,self.mode0_wgt,self.type0_wgt,self.chan0_wgt,self.butt0_wgt]
        self.items1      = [self.cond0_wgt,self.tmin0_wgt]
        self.box0        = VBox(children=self.items0,layout=self.vbox_layout)
        self.box1        = VBox(children=self.items1,layout=self.vbox_layout)
        self.ui0         = HBox(children=[self.box0,self.box1])
        self.ui1         = VBox(children=[self.ui0,self.output0_wgt])
        # Options and values
        temp_DataMNE_key = next(itertools.islice(self.SDF.keys(),2,3))
        temp_DataMNE_dat = self.SDF[temp_DataMNE_key]
        self.subj0_wgt.options   = list(self.SDF.keys())
        self.subj0_wgt.value     = temp_DataMNE_key
        self.epochs0_wgt.options = ["epochs0"]
        self.epochs0_wgt.value   = "epochs0"
        self.tmin0_wgt.options   = ["1","2","3","4","5","6","7","8"]
        self.tmin0_wgt.value     = ["1","2","3","5"]
        self.cond0_wgt.options   = ["verb","noun","noun_F","noun_M"]
        self.cond0_wgt.value     = ["verb","noun_F","noun_M"]
        # Observing
        self.subj0_wgt   .observe(self.subj0_upd)
        self.epochs0_wgt .observe(self.epochs0_upd)
        self.tool0_wgt   .observe(self.tool0_upd)
        self.mode0_wgt   .observe(self.mode0_upd)
        self.type0_wgt   .observe(self.type0_upd)
        self.chan0_wgt   .observe(self.chan0_upd)

        self.subj0_upd(self,self.subj0_wgt)
        self.butt0_wgt.on_click(self.butt0_click)
        display(self.ui1)

        """
        options=self.df0.epochs0.unique().tolist()
        self.df0            = df0.copy()
        self.df1            = self.df0.copy()[["epochs0","tool0","mode0","type0","cond0","chan0","later0","front0","clust0"]].drop_duplicates()


        """


    def butt0_click(self,b):
        with self.output0_wgt:
            clear_output()
            self.g_function(
                subj0   = self.subj0_wgt,
                epochs0 = self.epochs0_wgt,
                tool0   = self.tool0_wgt,
                mode0   = self.mode0_wgt,
                type0   = self.type0_wgt,
                chan0   = self.chan0_wgt,
                cond0   = self.cond0_wgt,
                tmin0   = self.tmin0_wgt
        )

    def subj0_upd(self,*args):
        epochs0s = dc([key0 for key0 in self.SDF[self.subj0_wgt.value].keys() if key0.startswith("epochs")])
        self.SUBJ = self.SDF[self.subj0_wgt.value]
        self.epochs0_wgt.options = epochs0s
        self.epochs0_wgt.value   = epochs0s[0]
        self.epochs0_upd(*args)

    def epochs0_upd(self,*args):
        self.df1 = self.SDF[self.subj0_wgt.value][self.epochs0_wgt.value]["FEATS"].copy()
        self.df0 = self.df1.copy() # TODO FIXME
        self.tool0_wgt.options = self.df1[
            (self.df1.epochs0 == self.epochs0_wgt.value)
        ].tool0.unique().tolist()
        # self.tool0_upd(*args)

    def tool0_upd(self,*args):
        self.mode0_wgt.options = self.df1[
            (self.df1.epochs0 == self.epochs0_wgt.value) &
            (self.df1.tool0   == self.tool0_wgt  .value)
        ].mode0.unique().tolist()
        self.mode0_upd(*args)

    def mode0_upd(self,*args):
        self.type0_wgt.options = self.df1[
            (self.df1.epochs0 == self.epochs0_wgt.value) &
            (self.df1.tool0   == self.tool0_wgt  .value) &
            (self.df1.mode0   == self.mode0_wgt  .value)
        ].type0.unique().tolist()
        self.type0_upd(*args)

    def type0_upd(self,*args):
        self.chan0_wgt.options = self.df1[
            (self.df1.epochs0 == self.epochs0_wgt.value) &
            (self.df1.tool0   == self.tool0_wgt  .value) &
            (self.df1.mode0   == self.mode0_wgt  .value) &
            (self.df1.type0   == self.type0_wgt  .value)
        ].chan0.unique().tolist()
        self.chan0_upd(*args)

    def chan0_upd(self,*args):
        self.cond0_wgt.options = self.df1[
            (self.df1.epochs0 == self.epochs0_wgt.value) &
            (self.df1.tool0   == self.tool0_wgt  .value) &
            (self.df1.mode0   == self.mode0_wgt  .value) &
            (self.df1.type0   == self.type0_wgt  .value) &
            (self.df1.chan0   == self.chan0_wgt  .value)
        ].cond0.unique().tolist()
        # self.cond0_wgt.value=["verb","noun","noun_F","noun_M"]

    def g_function(self,epochs0,tool0,mode0,type0,chan0,cond0,subj0,tmin0):
        clear_output()
        plt.close("all")
        subj0   = self.subj0_wgt.value
        epochs0 = self.epochs0_wgt.value
        tool0   = self.tool0_wgt.value
        mode0   = self.mode0_wgt.value
        type0   = self.type0_wgt.value
        chan0   = self.chan0_wgt.value
        cond0   = self.cond0_wgt.value
        tmin0   = self.tmin0_wgt.value


        time0s = {key0:val0 for key0,val0 in self.SDF.meta["time"]["spans0"].items() if key0 in tmin0}


        self.df2 = self.df0[
            (self.df0.epochs0 == epochs0) &
            (self.df0.tool0   == tool0  ) &
            (self.df0.mode0   == mode0  ) &
            (self.df0.type0   == type0  ) &
            (self.df0.chan0   == chan0  ) &
            (self.df0.subj0   == subj0  )
        ].copy()
        if not cond0:
            # cond0 = self.df2.cond0.unique().tolist()
            cond0 = ["verb","noun_F","noun_M",]
            cond0 = [c0 for c0 in self.df2.cond0.unique().tolist() if c0 in cond0]

        if chan0 in ["FL","CL","PL","FR","CR","PR",]:
            chan0 = {chan0:self.SUBJ.meta["bund"]["base0"][chan0]}

        plt.ioff()
        fig = self.SUBJ.plot_evoked_comparison(
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
        # display(fig)
        plt.show(fig)


        self.df3 = self.df2[self.df2.cond0.isin(cond0)].copy()
        display(self.df3)
        display(self.df3.shape)

        """


        """
