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


class SummaryMNE():
    def __init__(self,df0,within=["cond0","clust0"],dv="valX",height=4,aspect=1):
        self.df0            = df0.copy()
        self.df1            = self.df0.copy()[["epochs0","tool0","mode0","type0","cond0","chan0","later0","front0","clust0","tmin0"]].drop_duplicates()
        self.within         = within
        self.dv             = dv
        self.height         = height
        self.aspect         = aspect
        self.drop_layout    = Layout(width="auto")
        self.butt_layout    = Layout(width="auto",height="auto")
        self.vbox_layout    = Layout(display="flex",flex_flow="col",align_items="stretch",width="50%")
        self.epochs0_widget = Dropdown(description="epochs0",layout=self.drop_layout,options=self.df0.epochs0.unique().tolist())
        self.tool0_widget   = Dropdown(description="tool0"  ,layout=self.drop_layout)
        self.mode0_widget   = Dropdown(description="mode0"  ,layout=self.drop_layout)
        self.type0_widget   = Dropdown(description="type0"  ,layout=self.drop_layout)
        self.tmin0_widget   = Dropdown(description="tmin0"  ,layout=self.drop_layout)
        self.cond0_widget   = SelectMultiple(description="cond0",layout=self.drop_layout,options=["verb","noun","noun_F","noun_M"],value=["verb","noun","noun_F","noun_M"],rows=9)
        self.butt0_widget   = Button(description="RUN! (pingouin.rm_anova)",button_style="danger",layout=self.butt_layout)
        self.output0_widget = Output(layout={"width":"100%","min_height":"6in","border":"1px solid red"})
        self.items0         = [self.epochs0_widget,self.tool0_widget,self.mode0_widget,self.type0_widget,self.tmin0_widget,self.butt0_widget]
        self.items1         = [self.cond0_widget]
        self.box0           = VBox(children=self.items0,layout=self.vbox_layout)
        self.box1           = VBox(children=self.items1,layout=self.vbox_layout)
        self.ui0            = HBox(children=[self.box0,self.box1])
        self.ui1            = VBox(children=[self.ui0,self.output0_widget])
        self.epochs0_widget .observe(self.epochs0_updated)
        self.tool0_widget   .observe(self.tool0_updated)
        self.mode0_widget   .observe(self.mode0_updated)
        self.type0_widget   .observe(self.type0_updated)
        self.tmin0_widget   .observe(self.tmin0_updated)
        # interactive**
        # interactive_output
        """
        self.interact       = interactive(
            self.g_function,
            **dict(
                epochs0 = self.epochs0_widget,
                tool0   = self.tool0_widget,
                mode0   = self.mode0_widget,
                type0   = self.type0_widget,
                tmin0   = self.tmin0_widget,
                cond0   = self.cond0_widget,
            ),
        )
        # display(self.UI,self.interact)
        # self.epochs0_widget.value = "epochs0"
        """
        self.epochs0_updated(self,self.epochs0_widget)
        self.butt0_widget.on_click(self.butt0_click)
        self.DESC  = "<first hit run!>"
        display(self.ui1)


    def info(self):
        print(self.DESC)

    def butt0_click(self,b):
        with self.output0_widget:
            clear_output()
            self.g_function(
                epochs0 = self.epochs0_widget,
                tool0   = self.tool0_widget,
                mode0   = self.mode0_widget,
                type0   = self.type0_widget,
                tmin0   = self.tmin0_widget,
                cond0   = self.cond0_widget,
        )

    """
    TODO: change order of updates
    - make tmin0 first

    """

    def epochs0_updated(self,*args):
        self.tool0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value)
        ].tool0.unique().tolist()
        self.tool0_updated(*args)

    def tool0_updated(self,*args):
        self.mode0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value)
        ].mode0.unique().tolist()
        self.mode0_updated(*args)

    def mode0_updated(self,*args):
        self.type0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value) &
            (self.df1.mode0   == self.mode0_widget  .value)
        ].type0.unique().tolist()
        self.type0_updated(*args)

    def type0_updated(self,*args):
        self.tmin0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value) &
            (self.df1.mode0   == self.mode0_widget  .value) &
            (self.df1.type0   == self.type0_widget  .value)
        ].tmin0.unique().tolist()
        self.tmin0_updated(*args)

    def tmin0_updated(self,*args):
        self.cond0_widget.options = self.df1[
            (self.df1.epochs0 == self.epochs0_widget.value) &
            (self.df1.tool0   == self.tool0_widget  .value) &
            (self.df1.mode0   == self.mode0_widget  .value) &
            (self.df1.type0   == self.type0_widget  .value) &
            (self.df1.tmin0   == self.tmin0_widget  .value)
        ].cond0.unique().tolist()
        # self.cond0_widget.value=["verb","noun","noun_F","noun_M"]

    def g_function(self,epochs0,tool0,mode0,type0,tmin0,cond0):
        epochs0 = self.epochs0_widget.value
        tool0   = self.tool0_widget.value
        mode0   = self.mode0_widget.value
        type0   = self.type0_widget.value
        tmin0   = self.tmin0_widget.value
        cond0   = self.cond0_widget.value
        self.df2 = self.df0[
            (self.df0.epochs0 == epochs0) &
            (self.df0.tool0   == tool0  ) &
            (self.df0.mode0   == mode0  ) &
            (self.df0.type0   == type0  ) &
            (self.df0.tmin0   == tmin0  )
        ].copy()
        if not cond0:
            cond0 = self.df2.cond0.unique().tolist()

        self.df3 = self.df2[self.df2.cond0.isin(cond0)].copy()
        self.ARGS = OrderedDict()
        self.ARGS["data"]       = self.df3.copy()
        self.ARGS["within"]     = self.within
        self.ARGS["dv"]         = self.dv
        self.ARGS["subject"]    = "subj0"
        self.ARGS["correction"] = "auto"
        self.ARGS["detailed"]   = False
        self.ARGS["effsize"]    = "np2" # "np2" "n2" "ng2"
        self.AOV  = pg.rm_anova(**self.ARGS).round(3)
        display(self.AOV)
        self.N = self.df3.shape[0]
        self.DESC = "epochs0: {}".format(epochs0)
        self.DESC = "; ".join([self.DESC,"tool0:{}"  .format(tool0      )])
        self.DESC = "; ".join([self.DESC,"mode0:{}"  .format(mode0      )])
        self.DESC = "; ".join([self.DESC,"type0:{}"  .format(type0      )])
        self.DESC = "; ".join([self.DESC,"tmin0:{}"  .format(tmin0      )])
        self.DESC = "; ".join([self.DESC,"cond0:{}"  .format(cond0      )])
        self.DESC = "; ".join([self.DESC,"within:{}" .format(self.within)])
        self.DESC = "; ".join([self.DESC,"dv:{}"     .format(self.dv    )])
        self.DESC = "; ".join([self.DESC,"N:{}"      .format(self.N     )])
        display(self.DESC)
        self.PLOT = sns.catplot(
            x       = self.ARGS["within"][1],
            y       = self.ARGS["dv"],
            hue     = self.ARGS["within"][0],
            data    = self.ARGS["data"],
            order   = ["FL","FR","CL","CR","PL","PR",],
            kind    = "bar",
            palette = "Set2",
            height  = self.height,
            aspect  = self.aspect,
        )
        plt.show()
        self.AVG0 = self.ARGS["data"].groupby("cond0").agg(["count","mean","std"])[self.dv]
        self.AVG1 = self.ARGS["data"].groupby(self.ARGS["within"]).agg(["count","mean","std"])[self.dv]
