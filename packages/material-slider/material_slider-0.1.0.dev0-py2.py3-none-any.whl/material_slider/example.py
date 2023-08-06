#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Dou Du.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Float, List 
from ._frontend import module_name, module_version


class MaterialSlider(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('MaterialSliderModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('MaterialSliderView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Float(0).tag(sync=True)
    width = Unicode('400px').tag(sync=True)
    marks = List().tag(sync=True)
    labels = List().tag(sync=True)
    title = Unicode('title').tag(sync=True)

    min = Float(0.0).tag(sync=True)
    max = Float(100.0).tag(sync=True)
    step = Float(1.0).tag(sync=True)
    

