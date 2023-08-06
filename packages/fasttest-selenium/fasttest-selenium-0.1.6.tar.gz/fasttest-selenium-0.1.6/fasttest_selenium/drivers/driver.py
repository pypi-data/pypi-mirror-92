#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest_selenium.common import Var

class WebDriver(object):

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)


wd = WebDriver()
