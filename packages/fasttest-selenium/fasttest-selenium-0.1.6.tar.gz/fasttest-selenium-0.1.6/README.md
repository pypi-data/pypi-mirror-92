# 框架介绍
fasttest-selenium 是由Python语言开发的WEB端自动化框架，通过yaml编写相应的action即可调用Selenium API完成自动化测试。  
[文档介绍](https://www.yuque.com/books/share/99dcee33-a99d-4364-ab48-eb511d7ceb2d?#)
## idea
- 能否同时运行多个不同的浏览器，解决兼容性测试问题
- 通过插件快速输入关键字
## 已完成功能
- selenium 90%的Action支持
- 可拓展的公共方法和公共函数
- 高度还原steps的报告输出
## 待完成功能
- 数据类型优化：支持自定义复杂数据结构
- 结果报告优化：支持图片放大


# 快速体验
## 框架下载

fasttest-selenium已经发布到Python PyPi平台，可通过以下两种方式完成安装
1.在终端输入下方命令进行安装：

```bash
pip3 install fasttest-selenium
```

2.可前往[代码仓库](https://github.com/Jodeee/fasttest_selenium)直接clone或下载源码。

> 下载源码后需要将包导入到当前项目中

## 项目依赖

该框架在Python3.7版本下开发，部分功能依赖第三方模块，故需要安装以下模块

1. `PyYAML` 用于解析yaml测试用例文件

```basic
pip3 install PyYAML
```

2. `selenium` WEB自动化框架

```basic
pip3 install selenium
```

3. `colorama` 日志高亮输出

```basic
pip3 install colorama
```

4.`opencv-contrib-python` 图片对比识别

```basic
pip3 install opencv-contrib-python==3.4.2.16
```

> 说明：opencv在3.4.2以上版本使用其算法需要**授权确认**，该版本最高支持Python3.7，如不需要图片对比能力，可安装最新版Python和opencv-contrib-python

## 测试Demo

[Demo](https://github.com/Jodeee/fasttestSeleniumDemo)包含完整项目结构以及关键字测试用例，下载后可通过运行 `runtest.py` 启动测试执行

# 项目结构

## 项目树状图

```
├── Common           // 自定义关键字库  
|   ├── common.yaml  // 自定义关键字文件
├── Resource         // 文件资源目录
|   ├── test.png     // 图片资源
├── Report           // 结果报告目录  
├── Scripts          // 脚本函数目录 
|   ├── __init__.py  // 包标识文件
|   ├── test.py      // 脚本文件
├── TestCase         // 测试用例目录
|   ├── test.yaml    // 测试用例文件
├── config.yaml      // 项目配置文件  
├── data.json        // 数据配置文件  
├── runtest.py       // 项目执行文件
```

## config 项目配置

`config.yaml` 包含了项目运行时必要参数，结构如下：  
`driver` 固定参数，值为 `selenium`   
`browser` 指定浏览器，包括 `chrome` 、 `firefox` 、 `safari` 、 `ie` 、 `opera`   
`isReset` 每条用例执行完后是否重置浏览器，推荐设置为 `True` 
`saveScreenshot` 执行步骤是否保存截图，如果为`True` 将大大增加执行时间，推荐设置为 `False` ，只在执行异常时保存截图  
`implicitlyWait` 隐式等待时间  
`maxWindow` 窗口最大化  
`desiredcaps` 启动参数配置，会根据 `browser` 拿到对应浏览器参数  
`driver` 浏览器驱动，如驱动未添加环境变量中，可通过此参数指定驱动路径  
`options` 浏览器启动参数，会自动添加到对应浏览器的`options`  
`testcast` 用例执行路径，可指定某一条用例路径或者某一文件夹下面所有用例  


```yaml
driver: selenium
browser: chrome
isReset: True
saveScreenshot: False
implicitlyWait: 10
maxWindow: True
desiredcaps:
    - chrome:
        - driver: '/Users/xiongjunjie/Desktop/chromedriver'
          options: # 无头模式运行
            - '--headless'
            - '--dissble-gpu'
            - '--window-size=1920,1050'
      firefox:
        - driver: '/Users/xiongjunjie/Desktop/geckodriver'
          options:
            - '--headless'
            - '--dissble-gpu'
            - '--window-size=1920,1050'

testcase:
    - TestCase/common/
    - TestCase/selenium/cookies.yaml

```

## data 数据配置

`data.json` 为数据配置，结构如下：  
`variable` 全局变量配置，用例中可直接获取该配置下的数据  
`resource` 资源路径配置，用例中可直接访问该相对路径下的文件资源  
`keywords` 脚本函数配置，用例中可直接调用该配置下的函数  

```json
{
  "variable": {
    "userid": "admin",
    "password": 13456
  },
  "resource": {
    "baidu_logo": "Resource/baidu.png"
  },
  "keywords": [
    "keyDown",
    "getText"
  ]
}
```

例：直接调用 `keywords` 函数并传递userid的值和baidu_logo的路径

```yaml
- keyDown(${userid},${baidu_logo})
```

## runtest 执行入口

`runtest.py` 为整个项目执行入口，可直接执行该文件或在终端运行 `python3 runtest.py` 启动项目  
`start` 方法有返回整体执行结果，方便接入持续集成或者生成自定义报告           

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest_selenium import *

if __name__ == '__main__':

    project = Project()

    project.start()

```

## Common 自定义关键字

`Common` 目录用于存放自定义的关键字，类似于PO模式中的Page，可以将用例中公共逻辑抽离出来保存到这里，它需要一个关键字来表达它的作用，所以我们需要为它指定一个唯一的名字，以便于我们在用例中可调用。  
**关键字结构：**  
`common_action` 关键字名称，性感且唯一  
`description` 关键字描述，简短有力  
`input`  传入参数，一个不漏  
`output` 返回参数，暂未实现  
`steps` 执行步骤  
关键字定义：

```yaml
common_action:        
 description: 公共方法
 input: [key,value]
 output: []
 steps:
    - click(${value})
    - sleep(5)
    
common_action1:        
 description: 公共方法1
 input: [key,value]
 output: []
 steps:
    - click(${value})
    - sleep(5)
```

调用方式：在用例中call + 关键字名称为调用该关键字的语法，参数个数应和 `input` 相对应

```yaml
- call common_action('key','测试数据')
```

## Scripts 脚本函数

`Scripts` 为Python脚本目录，在 [`data.json`]下 `keywords` 中注册方法名后，就可直接在用例中调用脚本
如现有关键字无法完成的特殊操作，可以导入框架中 `driver` 模块，通过 `driver` 调用底层API  
函数定义：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest_selenium.driver import *

def getText():
    '''
    调用selenium api获取当前页面标题
    '''
    log_info(driver.title)
    return driver.title

def getTest(test):
    '''
    普通函数
    '''
    log_info(test)
```

调用方式：如果需要拿到函数返回的数据，可以直接用变量保存，如不需要，可以直接调用函数

```yaml
- ${title} = getText() # 获取返回值
- getTest('测试数据') # 普通函数
```

## Resource 文件资源

`Resource` 目录下的文件资源在 [`data.json`](#nNDdu) 下 `resource` 中指定文件名称和相对路径后，可以直接在用例中访问该资源文件

```yaml
- matchImage(${baesImage}, ${baidu_logo})
```

## TestCase 测试用例

`TestCase` 用于存放测试用例，测试用例为 `YAML` 文件，如果对`YAML` 语法不熟悉可参考[菜鸟教程](https://www.runoob.com/w3cnote/yaml-intro.html)，用例结构如下：  
`module` 用例所属业务模块，同一业务下用例的`module` 应保持一致，在结果报告中它们将展示在同一个分组下面  
`skip` 是否跳过该用例，默认为false  
`description` 用例描述  
`steps` 用例步骤  

```yaml
module: selenium
skip: false
description: action相关
steps:
  - openUrl('https://www.baidu.com')
  # 检查元素
  - check('id=su')
  # 单击元素
  - click('id=su')
  # 右击元素
  - contextClick('id=su')
  # 双击元素
  - doubleClick('class=hot-refresh-text')
  # 按住鼠标左键
  - holdClick('class=hot-refresh-text')
```

## Report 结果报告

`Report` 为测试结果目录，用例执行完毕后会自动生成高度还原测试用例步骤的测试报告，可点击具体步骤
查看截图和错误信息

# 关键字

测试用例中的关键字包含4中场景，项目结构中已经介绍了自定义关键字 [`Common`](https://www.yuque.com/jodeee/vt6gkg/iqc0hn#yiqZY) 和 [`Scripts`](https://www.yuque.com/jodeee/vt6gkg/iqc0hn#YU0b2) ，接下来两种是固定关键字

## 讲在前面

在介绍关键字之前，先介绍下用例中经常用到的两个点

1. 关于变量的定义，占位符${} + 变量名test来表示这是一个变量，获取该变量同样如此
   1. 关于赋值：它可以直接被赋值或者其他关键字返回值给变量
   1. 关于取值：一条用例中${test}会从多个地方尝试获取值，所以具有一定优先级
      1. 最高优先级：如果在for循环中，会优先获取for循环迭代值
      1. 第二优先级：如果for循环中无法获取该变量，会尝试从当前用例中获取变量值
      1. 第三优先级：如果当前用例中未定义该变量，会判断是否在 `Common` 库中 `input` 有定义
      1. 第四优先级：如果以上三种均未获取该变量，会尝试从 `data.json` 下 `variable` 、 `resource` 获取变量值
2. 元素定位方法：selenium有八种元素定位方式，为了简化步骤描述，用例中按照 `type=element` 的方式即可定位到相关元素
   1. 元素定位方式：_id、name、class、tag_name、link_text、partial_link_text、xpath、css_selector_
   1. 例：点击百度按钮 click("id=su") 

![image.png](https://cdn.nlark.com/yuque/0/2020/png/499819/1608438016248-05bad871-ec48-4fb6-a6f1-c8bfc1c5ba62.png#align=left&display=inline&height=685&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1370&originWidth=2822&size=634969&status=done&style=none&width=1411)

## Selenium Action

### Browser

#### 打开网页(openUrl)

`openUrl` 打开一个网页，参数: `URL` 

```yaml
- ${url} = 'https://www.baidu.com'
- openUrl(${url})
# 或者
- openUrl('https://www.baidu.com')
```

对应Selenium API ：

```python
driver = webdriver.Chrome()
driver.get(url)
```

#### 关闭标签页或窗口(close)

`close` 关闭当前标签页或窗口

```yaml
- openUrl('https://www.baidu.com')
- close()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.close()
```

#### 后退(back)

`back` 退回到上一页

```yaml
- back()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.find_element_by_xpath('//*[@id="s-top-left"]/a[1]').click()
driver.back()
```

#### 前进(forward)

`forward` 前进到下一页

```yaml
- forward()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.find_element_by_xpath('//*[@id="s-top-left"]/a[1]').click()
driver.back()
driver.forward()
```

#### 刷新(refresh)

`refresh` 刷新当前页面

```yaml
- refresh()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.refresh()
```

#### 窗口最大化(maxWindow)

`maxWindow` 窗口最大化

```yaml
- maxWindow()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
```

#### 窗口最小化(minWindow)

`minWindow` 窗口最小化

```yaml
- minWindow()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.minimize_window()
```

#### 窗口全屏(fullscreenWindow)

`fullscreenWindow` 窗口全屏

```yaml
- fullscreenWindow()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.fullscreen_window()
```

#### 设置窗口大小(setWindowSize)

`setWindowSize` 设置窗口大小，参数： `width` ， `height` 

```yaml
- setWindowSize(3000,2000)
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.set_window_size(3000,2000)
```

#### 设置窗口坐标(setWindowPosition)

`setWindowPosition` 设置窗口起始坐标，参数： `x` ， `y` 

```yaml
- setWindowPosition(10,20)
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.set_window_position(10,20)
```

#### 获取窗口大小($.getWindowSize)

`$.getWindowSize` 获取窗口大小

```yaml
- ${w_size} = $.getWindowSize()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
w_size = driver.get_window_size()
```

#### 获取窗口坐标($.getWindowPosition)

`$.getWindowPosition` 获取窗口起始坐标

```yaml
- ${w_position} = $.getWindowPosition()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
w_position = driver.get_window_position()
```

#### 获取当前窗口句柄($.getCurrentWindowHandle)

`$.getCurrentWindowHandle` 获取当前窗口句柄

```yaml
- ${handle} = $.getCurrentWindowHandle()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
handle = driver.current_window_handle
```

#### 获取所有窗口句柄($.getWindowHandles)

`$.getWindowHandles` 获取所有窗口句柄

```yaml
- ${handles} = $.getWindowHandles()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
handles = driver.window_handles
```

#### 切换窗口句柄(switchToWindow)

`switchToWindow` 切换窗口句柄，参数: `handle` 

> 获取所有的窗口句柄是无序的，建议用for循环切换窗口句柄

```yaml
- ${all_handle} = $.getWindowHandles()
- for ${handle} in ${all_handle}:
    # 切换窗口句柄
    - switchToWindow(${handle})
    - ${title} = $.getTitle()
    - if ${title} == '百度新闻——海量中文资讯平台':
        - break
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
handles = driver.window_handles
for handle in handles:
    # 切换窗口句柄
    switch_to.window(handle)
    title = driver.title
    if title == '百度新闻——海量中文资讯平台':
        break
```

#### 获取窗口标题($.getTitle)

`$.getTitle` 获取窗口标题

```yaml
- ${title} = $.getTitle()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
title = driver.title
```

#### 获取窗口URL($.getCurrentUrl)

`$.getCurrentUrl` 获取窗口URL

```yaml
- ${title} = $.getCurrentUrl()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
title = driver.current_url
```

#### 获取浏览器名称($.getName)

`$.getName` 获取浏览器名称

```yaml
- ${name} = $.getName()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
title = driver.name
```


### Action

#### 单击(click)

`click` 鼠标左键单击，参数: `element` 

```yaml
- click('id=su')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_id('su')
element.click()
```

#### 右击(contextClick)

`contextClick` 鼠标右键单击，参数: `element`

```yaml
- contextClick('id=su')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_id('su')
ActionChains(driver).context_click(element).perform()
```

#### 双击(doubleClick)

`doubleClick` 鼠标左键双击，参数: `element`

```yaml
- doubleClick('id=su')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_id('su')
ActionChains(driver).double_click(element).perform()
```

#### 长按(holdClick)

`holdClick` 长按鼠标左键不放，参数: `element`

```yaml
- holdClick('id=su')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_id('su')
ActionChains(driver).click_and_hold(element).perform()
```

#### 拖放元素到另一个元素位置(dragDrop)

`dragDrop` 拖放元素到另一个元素位置，参数: `element`，`target`

```yaml
- dragDrop('xpath=//*[@id="sbox"]/tbody/tr/td[1]/div[1]/a/img','id=s_btn_wr')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_xpath('//*[@id="sbox"]/tbody/tr/td[1]/div[1]/a/img')
target = find_element_by_id('s_btn_wr')
ActionChains(driver).drag_and_drop(element, target).perform()
```

#### 拖放元素到某个位置(dragDropByOffset)

`dragDropByOffset` _拖放元素到某个位置_，参数: `element` ， `x` ， `y` 

```yaml
- dragDropByOffset('xpath=//*[@id="sbox"]/tbody/tr/td[1]/div[1]/a/img',10,10)
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_xpath('//*[@id="sbox"]/tbody/tr/td[1]/div[1]/a/img')
ActionChains(driver).drag_and_drop_by_offset(element, 10, 10).perform()
```

#### 鼠标移动到某个位置(moveByOffset)

`moveByOffset` _鼠标从当前位置移动到某个坐标_，参数：`x` ， `y`

```yaml
- moveByOffset(10,10)
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
ActionChains(driver).move_by_offset(10, 10).perform()
```

#### 鼠标移动到某个元素(moveToElement)

`moveToElement` _鼠标移动到某个元素上_，参数: `element`

```yaml
- moveToElement('xpath=//*[@id="hotsearch-content-wrapper"]/li[1]/a/span[2]')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_xpath('//*[@id="hotsearch-content-wrapper"]/li[1]/a/span[2]')
ActionChains(driver).move_to_element(element).perform()
```

#### 鼠标_移动到距某个元素多少距离的位置_(moveToElementWithOffset)

`moveToElementWithOffset` 鼠标_移动到距某个元素(左上角坐标)多少距离的位置_，参数: `element` ， `x` ， `y`

```yaml
- moveToElementWithOffset('id=su',10,20)
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_id('su')
ActionChains(driver).move_to_element_with_offset(element, 10, 20).perform()
```

#### 输入(sendKeys)

`sendKeys` 输入文案，参数： `element` ， `Keys(可选)` ， `text` 

```yaml
- sendKeys('name=wd','测试文案') # 普通输入
# 复制粘贴
- sendKeys('name=wd','Keys.CONTROL', 'c') # control + c
- sendKeys('name=wd','Keys.CONTROL', 'v') # control + v
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_name('wd')
element.send_keys('测试文案')
# 复制粘贴
element.send_keys(Keys.CONTROL, 'c')
element.send_keys(Keys.CONTROL, 'v')
```

#### 清除(clear)

`clear` 清除输入框文案、元素选中状态

```yaml
- clear('name=wd')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_name('wd')
element.clear()
```

#### 执行JS(executeScript)

`executeScript` 执行JS代码，参数: `script`   

```yaml
- ${js} = "window.open('http://www.taobao.com')"
- executeScript(${js})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
js = "window.open('http://www.taobao.com')"
driver.execute_script(js)
```

#### 截图($.saveScreenshot)

`$.saveScreenshot` 对屏幕或者元素截图，参数: `element(可选，如果为空则截全屏)`， `name`   

```yaml
# 对元素截图，返回图片路径
- ${path} = $.saveScreenshot('id=su', 'biadu.png')
# 全屏截图，返回图片路径
- ${path} = $.saveScreenshot('biadu.png')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element = find_element_by_id('su')
# 元素截图
element.screenshot(path)
# 全屏截图
driver.save_screenshot(path)
```

### Element

#### 获取单个元素($.getElement)

`$.getElement` 获取单个元素，参数: `element`   

```yaml
# 获取单个元素 id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector
- ${element_id} = $.getElement('id=su')
- ${element_name} = $.getElement('name=f')
- ${element_class} = $.getElement('class=s_ipt')
- ${element_tag_name} = $.getElement('tag_name=form')
- ${element_link_text} = $.getElement('link_text=新闻')
- ${element_partial_link_text} = $.getElement('partial_link_text=新')
- ${element_xpath} = $.getElement('xpath=//*[@id="su"]')
- ${element_css_selector} = $.getElement('css_selector=[name="wd"]')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
'''
        by = Dict({
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'class': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'css_selector': By.CSS_SELECTOR,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
        })
'''
element_id = find_element(By.ID, 'su')
```

#### 获取多个元素($.getElement)

`$.getElement` 获取单个元素，参数: `element`   

```yaml
# 获取多个元素 id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector
- ${elements_class} = $.getElements('class=title-content-title')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
elements_class = find_elements(By.CLASS_NAME, 'title-content-title')
```

#### 判断元素是否选中($.isSelected)

`$.isSelected` 判断元素是否选中，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${is_selected} = $.isSelected(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
is_selected = element_id.is_selected()
```

#### 判断元素是否显示($.isDisplayed)

`$.isDisplayed` 判断元素是否显示，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${is_displayed} = $.isDisplayed(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
is_displayed = .is_displayed()
```

#### 判断元素是否可用($.isEnabled)

`$.isEnabled` 判断元素是否可用，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${is_enabled} = $.isEnabled(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
is_enabled = element_id.is_enabled()
```

#### 获取元素大小($.getSize)

`$.getSize` 判断元素是否选中，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${size} = $.getSize(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
size = element_id.size
```

#### 获取元素坐标($.getLocation)

`$.getLocation` 获取元素坐标，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${location} = $.getLocation(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
location = element_id.location
```

#### 获取元素位置大小($.getRect)

`$.getRect` 获取元素位置大小，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${rect} = $.getRect(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
rect = element_id.rect
```

#### 获取元素标签($.getTagName)

`$.getTagName` 获取元素标签，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${tag} = $.getTagName(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
tag = element_id.tag_name
```

#### 获取元素文案($.getText)

`$.getText` 获取元素位置文案，参数: `element`   

```yaml
- ${element_id} = $.getElement('id=su')
- ${text} = $.getText(${element_id})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
text = element_id.text
```

#### 获取元素属性($.getAttribute)

`$.getAttribute` 获取元素位置属性，参数: `element` ， `attribute` 

```yaml
- ${element_id} = $.getElement('id=su')
- ${attribute} = $.getAttribute(${element_id}, 'value')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
attribute = element.get_attribute('value')
```

#### 获取元素CSS($.getCssProperty)

`$.getCssProperty` 获取元素CSS，参数: `element` ， `css` 

```yaml
- ${element_id} = $.getElement('id=su')
- ${css} = $.getCssProperty(${element_id}, 'height')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
element_id = find_element(By.ID, 'su')
css = element_id.value_of_css_property('height')
```

### 

### Cookie

#### 获取所有Cookie($.getCookies)

`$.getCookies` 获取所有Cookie

```yaml
- ${cookies} = $.getCookies()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
cookies = driver.get_cookies()
```

#### 获取指定Cookie($.getCookie)

`$.getCookie` 获取指定Cookie，参数: `name`

```yaml
- ${cookie} = $.getCookie('BAIDUID')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
cookie = driver.get_cookie('BAIDUID')
```

#### 删除指定Cookie(deleteCookie)

`deleteCookie` 删除指定Cookie，参数: `name`

```yaml
- deleteCookie('BAIDUID')
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.delete_cookie('BAIDUID')
```

#### 删除所有Cookie(_deleteAllCookies_)

`deleteAllCookies` 删除所有Cookie

```yaml
- deleteAllCookies()
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
driver.delete_all_cookies()
```

#### 添加指定Cookie(addCookie)

`addCookie` 添加指定Cookie，参数: `cookie`

```yaml
- ${add_cookie} = {'name':'ADDCOOKIE','value':'123adc'}
- addCookie(${add_cookie})
```

对应Selenium API：

```python
driver = webdriver.Chrome()
driver.get(url)
add_cookie = {'name':'ADDCOOKIE','value':'123adc'}
driver.add_cookie(add_cookie)
```


## Other Action

### **变量(**${variables}**)**

关于变量已经在开头介绍过，这里演示变量几种写法

```yaml
# 直接赋值
- ${t1} = 1
- ${t2} = '2'
- ${t3} = "3"
- ${t4} = True
- ${t5} = False
- ${t6} = None
- ${t7} = [1,2,3]
- ${t8} = {'key':'value'}
# 调用方法返回
- ${elements} = $.getElements('class=title-content-title')
```

如果变量值为列表或字典，可以指定index或者key来获取其中某一个元素的值

```yaml
- keyDown(${7}[0], ${t8}['key'])
```

### 设置全局变量(setVar)**

`setVar` 设置全局变量，该变量在整个测试执行结束后才会销毁，参数： `key` ， `value` 

```yaml
- setVar('key','测试')
```

### 获取全局变量($.getVar)**

`$.getVar` 获取全局变量，参数： `key`

```yaml
- ${test} = $.getVar('key')
```

### 获取长度($.getLen)

`$.getLen` 可以获取其他变量的长度，这对于循环是有帮助的，参数： `variables` 

```yaml
- ${t7} = [1,2,3]
- ${len} = $.getLen(${t7})
```

### 睡眠(sleep)

`sleep` 在当前步骤等待指定时间，参数： `s` 

```yaml
- sleep(5) # 等待5s
```

### 断言(assert)

`assert` 用例中可以直接断言来检查执行是否符合预期效果，参数：`条件表达式` 

```yaml
- assert 5 > 4
- ${text} = '测试文案'
- assert '文案' == ${text}
- assert '文案' in '测试文案'
```

### 执行表达式($.id)

`$.id` 用于执行一个表达式，参数：`表达式`

```yaml
- ${index} = $.id(1+1) # 2
- ${str} = $.id('测试'+'文案') # 测试文案
```

### 条件语句(if、elif、else)

`if` 、 `elif` 、 `else` 根据条件表达式来决定执行代码，参数：`条件表达式`

```yaml
- ${index} = $.id(1+1) # 2
- if ${index} == 2:
    - ${test} = 1
  elif ${index} > 2:
    - ${test} = 2
  else:
    - ${test} = 3
```

### 循环语句(while)

`while` 用于循环执行程序， 参数：`条件表达式`
`break` 在某一条件成立时，可以跳出循环

```yaml
- ${list} = [1,2,3,4]
- ${len} = $.getLen(${list})
- while ${len}:
    - ${len} = $.id(${len}-1)
    - if ${list}[${len}] == 2:
      - break
```

### 循环语句(for)

`for` 循环可以遍历任何序列的项目，如一个列表或者一个字符串， 参数： `可迭代对象` 
`break` 在某一条件成立时，可以跳出循环

```yaml
# 打开URL
- openUrl('https://www.baidu.com')
# 打开一个新窗口  
- click('xpath=//*[@id="s-top-left"]/a[1]')
# 获取所有窗口句柄
- ${all_handle} = $.getWindowHandles()
# for 循环
- for ${handle} in ${all_handle}:
    # 切换窗口句柄
    - switchToWindow(${handle})
    - ${title} = $.getTitle()
    - if ${title} == '百度新闻——海量中文资讯平台':
        - break
```

# End
