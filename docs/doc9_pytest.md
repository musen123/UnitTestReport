#



### 1、pytest-testreport介绍
因为之前有小伙伴多次反馈，想使用pytest生成unittestreport的html报告,刚好之前雨泽老师写了个pytest生成报告的插件，于是在雨泽老师代码的基础上实现了pytest生产unittestreport报告。也就是pytest-testreport这个插件。


pytest-testreport是一个针对pytest的生成html报告的插件，使用起来非常简单，只需要再pytest.ini文件中做简单的配置即可实现html报告的生成


### 2、安装pytest-testreport

pytest-testreport是基于python3.6开发的，安装前请确认你的python版本>3.6

安装命令

```pip install pytest-testreport```

### 3、使用方式：

**方式一：**在pytest.ini文件加入配置块`[report]`，即可实现生成html报告

```ini
[report]
```
    
支持的配置：报告文件名，报告标题、测试者名称、报告概要描述。
```ini
[report]
file_name = report.html
title = test report
tester = tester
desc = test desc
```
    
**注意点**：如果在pytest.ini文件中写入中文，运行时出现可能出现如下错误(pytest加载配置文件本身的问题和插件无关)![1621323815016](./img/1621323815016.png)

**解决办法：修改pytest.ini文件的编码为GBK**
    
    
    
**方式二：** pytest 运行测试时加上参数--report 指定报告文件名

    ```pytest --report=musen.html```










