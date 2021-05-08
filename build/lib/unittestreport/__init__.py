"""
============================
Author:柠檬班-木森
Time:2020/7/16   16:25
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
unittestreport基于unittest扩展了5个功能：
1、html测试报告的生成(三个风格)
2、测试用例失败重运行
3、测试报告邮件发送功能
4、数据驱动
5、多线程执行测试用例
"""

from .core.testRunner import TestRunner,Load
from .core.dataDriver import ddt, list_data, json_data, yaml_data
from .core.reRun import rerun
