#



### 1、pytest-testreport介绍
因为之前有小伙伴多次反馈，想使用pytest生成unittestreport的html报告,刚好之前雨泽老师写了个pytest生成报告的插件，于是在雨泽老师代码的基础上实现了pytest生产unittestreport报告。也就是pytest-testreport这个插件。


pytest-testreport是一个针对pytest的生成html报告的插件，使用起来非常简单，只需要再pytest.ini文件中做简单的配置即可实现html报告的生成


### 2、安装pytest-testreport

pytest-testreport是基于python3.6开发的，安装前请确认你的python版本>3.6

安装命令

```pip install pytest-testreport```

### 3、使用方式：


注意点：如果安装了pytest-html这个插件，请先卸载，不然会有冲突


*命令行执行* 
    

    运行测试时加上参数--report 指定报告文件名
    
    pytest --report=musen.html
    
    其他配置参数
    --title=指定报告标题
    --tester=指定报告中的测试者
    --desc = 指定报告中的项目描述
    --template = 指定报告模板样式（1 or 2）
    
    同时使用多个参数
    pytest --report=musen.html --title=测试报告 --tester=测试菜鸟 --desc=项目描述  --template=2
    
    
*pytest.main执行*

    
    import pytest
    
    pytest.main(['--report=musen.html',
                 '--title=测试报告标题',
                 '--tester=木森',
                 '--desc=报告描述信息',
                 '--template=2'])
    










