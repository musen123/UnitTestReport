#

##  1、什么是unittestreport

unittestreport是基于`unittest`开发的的一个功能扩展库，关于unittestreport最初在开发的时候，最初只是计划开发一个unittest生成html测试报告的模块，所以起名叫做unittestreport。在开发的过程中结合使用者的反馈，慢慢的扩展了更多的功能进去。后续还会持续的扩展和开发一些新的功能，目前实现了以下功能：

- HTML测试报告生成
- unittest数据驱动
- 测试用例失败重运行
- 多线程并发执行用例
- 发送测试结果及报告到邮箱
- 测试结果推送到钉钉
- 测试结果推送到企业微信

大家在使用的过程中，发现有bug或者有一些更好的建议，可以通过邮件反馈给我！

- **开发者：柠檬班-木森**
- **email：musen_nmb@qq.com**
## 2、安装unittestreport

unittestreport是基于python3.6开发的，安装前请确认你的python版本>3.6

- **安装命令**

    `pip install unittestreport`


## 3、pytest的支持

之前有小伙伴反馈，能不能让unittestreport支持pytest生成报告，所以就加上了这个功能。pytest生成unittestreport风格的报告，安装如下插件即可,详细教程见【第九节】

- **pytest插件安装命令**

    `pip install pytest-testreport`
