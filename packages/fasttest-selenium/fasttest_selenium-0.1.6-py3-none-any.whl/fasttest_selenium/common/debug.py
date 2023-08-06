#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdb
from fasttest_selenium.drivers.driver_base import DriverBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, InvalidSessionIdException, TimeoutException

def debug(func, *args, **kwds):
    def wrapper(*args, **kwds):
        '''
        by
        - 'id': By.ID
        - 'name': By.NAME
        - 'xpath': By.XPATH
        - 'class': By.CLASS_NAME
        - 'tag_name': By.TAG_NAME
        - 'link_text': By.LINK_TEXT
        - 'css_selector': By.CSS_SELECTOR
        - 'partial_link_text': By.PARTIAL_LINK_TEXT
        e.g.
        - element = driver.find_element(By.XPATH, 'value')
        - elements = driver.find_elements(By.XPATH, 'values')
        docs
        - https://www.selenium.dev/documentation/zh-cn/webdriver/web_element/
        '''
        is_debug = args[1].step
        try:
            if is_debug.endswith('--Debug') or is_debug.endswith('--debug'):
                driver = DriverBase.get_driver()
                pdb.set_trace()
            if args or kwds:
                result = func(*args, **kwds)
            else:
                result = func()
        except Exception as e:
            raise e
        return result
    return wrapper