#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def return_keywords():
    keywords = [
        "openUrl",  # 打开地址
        "close",  # 关闭标签页或窗口
        "submit",  # 提交表单
        "back",  # 后退
        "forward", # 前进
        "refresh", # 刷新
        "check",  # 检查元素
        "queryDisplayed", # 等待元素可见
        "queryNotDisplayed", # 等待元素不可见
        "click",  # 单击
        "contextClick",  # 右击
        "doubleClick",  # 双击
        "holdClick",  # 按下鼠标左键
        "dragDrop",  # 鼠标拖放
        "dragDropByOffset", # 拖动元素到某个位置
        "moveByOffset", # 鼠标从当前位置移动到某个坐标
        "moveToElement",  # 鼠标移动
        "moveToElementWithOffset", #移动到距某个元素(左上角坐标)多少距离的位置
        # "keyDownAndkeyUp", # 按下某个键盘上的键
        "sendKeys",  # 输入
        "clear",  # 清除
        "maxWindow",  # 窗口最大化
        "minWindow",  # 窗口最小化
        "fullscreenWindow", # 全屏窗口
        "setTimeout", # 设置等待时间
        "deleteAllCookies",  # 删除所有cookies
        "deleteCookie",  # 删除指定cookies
        "addCookie", # 添加cookies
        "switchToFrame", # 切换到指定frame
        "switchToDefaultContent", # 切换到主文档
        "switchToParentFrame", # 切回到父frame
        "switchToWindow", # 切换句柄
        "setWindowSize",  # 设置窗口大小
        "setWindowPosition",  # 设置设置窗口位置
        "executeScript", # 执行JS
        "matchImage", # 匹配图片
        "$.executeScript", # 获取JS执行结果
        "$.saveScreenshot", # 截图
        "$.isSelected",  # 判断是否选中
        "$.isDisplayed",  # 判断元素是否显示
        "$.isEnabled",  # 判断元素是否被使用
        "$.getSize",  # 获取元素大小
        "$.getLocation",  # 获取元素坐标
        "$.getRect", # 获取元素位置大小
        "$.getAttribute",  # 获取元素属性
        "$.getText",  # 获取元素文案
        "$.getTagName",  # 获取元素tag Name
        "$.getCssProperty",  # 获取元素css
        "$.getName",  # 获取浏览器名字
        "$.getTitle",  # 获取标题
        "$.getCurrentUrl", # 获取当前页面url
        "$.getCurrentWindowHandle", # 获取当前窗口句柄
        "$.getWindowHandles", # 获取所有窗口句柄
        "$.getCookies",  # 获取所有cookie
        "$.getCookie",  # 获取指定cookie
        "$.getWindowPosition",  # 获取窗口坐标
        "$.getWindowSize",  # 获取窗口大小
        "$.getElement",  # 获取元素
        "$.getElements",  # 获取元素
        "$.id",  # 科学运算
        "$.getLen", # 获取长度
        "$.getVar",  # 获取全局变量
        "setVar",  # 设置全局变量
        "sleep",
        "break",
        "while",
        "if",
        "elif",
        "else",
        # "ifcheck",
        # "elifcheck",
        "assert"
    ]

    return keywords

