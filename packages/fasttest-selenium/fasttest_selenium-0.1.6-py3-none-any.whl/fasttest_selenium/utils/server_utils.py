#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from fasttest_selenium.common import *



class ServerUtils(object):

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __init__(self, start_info):
        self.browser = start_info.browser.lower()
        self.instance = None
        self.options =start_info.options
        if start_info.max_window is None:
            max_window = False
        self.max_window = start_info.maxWindow
        self.remote = start_info.remote

    def start_server(self):

        try:
            if self.options and self.options.driver:
                if os.path.isfile(self.options.driver):
                    self.driver_path = self.options.driver
                else:
                    self.driver_path = None
                    log_error(' No such file : {}'.format(self.options.driver), False)
            else:
                self.driver_path = None

            if self.browser == 'chrome':
                options = webdriver.ChromeOptions()
                if self.options and self.options.options:
                    for opt in self.options.options:
                        options.add_argument(opt)
                if self.remote:
                    self.instance = webdriver.Remote(command_executor=self.remote,
                                                     desired_capabilities={
                                                         'platform': 'ANY',
                                                         'browserName': self.browser,
                                                         'version': '',
                                                         'javascriptEnabled': True
                                                     },
                                                     options=options)
                else:
                    if self.driver_path:
                        self.instance = webdriver.Chrome(executable_path=self.driver_path,
                                                     chrome_options=options)
                    else:
                        self.instance = webdriver.Chrome(chrome_options=options)
            elif self.browser == 'firefox':
                options = webdriver.FirefoxOptions()
                if self.options and self.options.options:
                    for opt in self.options.options:
                        options.add_argument(opt)
                if self.remote:
                    self.instance = webdriver.Remote(command_executor=self.remote,
                                                     desired_capabilities={
                                                         'platform': 'ANY',
                                                         'browserName': self.browser,
                                                         'version': '',
                                                         'javascriptEnabled': True
                                                     },
                                                     options=options)
                else:
                    if self.driver_path:
                        self.instance = webdriver.Firefox(executable_path=self.driver_path,
                                                        firefox_options=options)
                    else:
                        self.instance = webdriver.Firefox(firefox_options=options)
            elif self.browser == 'edge':
                if self.driver_path:
                    self.instance = webdriver.Edge(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.Edge()
            elif self.browser == 'safari':
                self.instance = webdriver.Safari()
            elif self.browser == 'ie':
                if self.driver_path:
                    self.instance = webdriver.Ie(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.Ie()
            elif self.browser == 'opera':
                if self.driver_path:
                    self.instance = webdriver.Opera(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.Opera()
            elif self.browser == 'phantomjs':
                if self.driver_path:
                    self.instance = webdriver.PhantomJS(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.PhantomJS()

            if self.max_window:
                self.instance.maximize_window()
            return self.instance
        except Exception as e:
            raise e

    def stop_server(self, instance):

        try:
            instance.quit()
        except Exception as e:
            raise e

