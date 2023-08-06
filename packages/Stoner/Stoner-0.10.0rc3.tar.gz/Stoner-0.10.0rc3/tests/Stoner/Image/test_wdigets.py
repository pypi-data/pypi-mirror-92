# -*- coding: utf-8 -*-
"""
Test the Image Widgets used for selections

@author: phygbu
"""
import pytest
from matplotlib.backend_bases import Event
import Stoner
import os
import threading
import time
import numpy as np

def _event(image,names,**kargs):
    """Make a fake event."""
    select=image._image._select
    event=Event("fake",select.fig.canvas)
    if not isinstance(names,list):
        names=[names]
    for name in names:
        for k,v in kargs.items():
            setattr(event,k,v)
        try:
            getattr(select,name)(event)
        except Exception as err:
            breakpoint()
            pass


def _trigger(image):
    time.sleep(1)
    _event(image,"on_click",xdata=1,ydata=1,button=1)
    for coord in np.linspace(1,100,51):
        _event(image,"draw_line",xdata=coord,ydata=coord)
    _event(image,"on_click",xdata=coord,ydata=coord,button=1)

def _trigger2(image):
    time.sleep(1)
    _event(image,"keypress",xdata=50,ydata=75,key="x")
    _event(image,"on_click",xdata=50,ydata=75,button=1)

def _trigger3(image):
    time.sleep(1)
    _event(image,"keypress",xdata=50,ydata=75,key="y")
    _event(image,"on_click",xdata=50,ydata=75,button=1)

def _trigger4(image):
    time.sleep(1)
    select=image._image._select
    event1=Event("fake",select.fig.canvas)
    event1.xdata=25
    event1.ydata=25
    event2=Event("fake",select.fig.canvas)
    event2.xdata=75
    event2.ydata=50
    select.on_select(event1,event2)
    _event(image,"finish",key="enter")


def _trigger5(image,mode):
    time.sleep(1)
    _event(image,["draw","on_click"],xdata=50,ydata=25,button=1,dblclick=False)
    _event(image,["draw","on_click"],xdata=75,ydata=50,button=1,dblclick=False)
    _event(image,"keypress",xdata=50,ydata=75,key=mode.lower()[0])
    if mode=="c": # add some extra points:
        _event(image,["draw","on_click"],xdata=30,ydata=40,button=1,dblclick=False)
        _event(image,["draw","on_click"],xdata=30,ydata=30,button=1,dblclick=False)
    _event(image,"keypress",xdata=50,ydata=75,key="i")
    _event(image,"keypress",xdata=50,ydata=75,key="enter")

def _trigger6(image,mode):
    time.sleep(1)
    _event(image,["draw","on_click"],xdata=50,ydata=25,button=1,dblclick=False)
    _event(image,["draw","on_click"],xdata=75,ydata=50,button=1,dblclick=False)
    _event(image,"keypress",xdata=50,ydata=75,key="escape")


def test_profile_line():
    os.chdir(Stoner.__homepath__/".."/"sample-data")
    img=Stoner.HDF5.STXMImage("Sample_Image_2017-10-15_100.hdf5")
    thread=threading.Thread(target=_trigger,args=(img,))
    thread.start()
    result = img.profile_line()
    assert len(result)==142
    assert result.x.min()==0.0
    assert np.isclose(result.x.max(),140,atol=0.01)
    assert np.isclose(result.y.mean(),26407.86,atol=0.01)
    thread=threading.Thread(target=_trigger2,args=(img,))
    thread.start()
    result = img.profile_line()
    assert len(result)==101
    assert result.x.min()==0.0
    assert result.x.max()==100.0
    assert np.isclose(result.y.mean(),20022.16,atol=0.01)
    thread=threading.Thread(target=_trigger3,args=(img,))
    thread.start()
    result = img.profile_line()
    assert len(result)==101
    assert result.x.min()==0.0
    assert result.x.max()==100.0
    assert np.isclose(result.y.mean(),27029.16,atol=0.01)

def test_regionSelect():
    os.chdir(Stoner.__homepath__/".."/"sample-data")
    img=Stoner.HDF5.STXMImage("Sample_Image_2017-10-15_100.hdf5")
    thread=threading.Thread(target=_trigger4,args=(img,))
    thread.start()
    result = img.crop()
    assert result.shape==(25,50)

def test_masking_select():
    os.chdir(Stoner.__homepath__/".."/"sample-data")
    img=Stoner.HDF5.STXMImage("Sample_Image_2017-10-15_100.hdf5")
    thread=threading.Thread(target=_trigger5,args=(img,"p"))
    thread.start()
    img.mask.select()
    result = img.mean()
    assert np.isclose(result,15731.6096)
    img.mask=False
    thread=threading.Thread(target=_trigger5,args=(img,"c"))
    thread.start()
    img.mask.select()
    result = img.mean()
    assert np.isclose(result,17380.52688172043)
    img.mask=False
    thread=threading.Thread(target=_trigger5,args=(img,"r"))
    thread.start()
    img.mask.select()
    result = img.mean()
    assert np.isclose(result,15745.5853061)
    img.mask=False
    thread=threading.Thread(target=_trigger6,args=(img,"c"))
    thread.start()
    img.mask.select()
    result = img.mean()
    assert np.isclose(result,27715.3245)


if __name__=="__main__": # Run some tests manually to allow debugging
    pytest.main(["--pdb",__file__])

