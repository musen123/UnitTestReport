# 

​	关于unittest重运行机制，unittestreport最新得版本中做了优化，直接使用TestRunner.run（之前的版本是TestRunner.rerun_run方法），传入相关的参数即可实现重运行，具体的使用如下

**案例**

运行时加上参数，即可实现用例失败重运行

```python
import unittestreport
# 1、加载测试用例到套件中
suite = unittest.defaultTestLoader.discover(r'C:\project\open_class\Py0507\testcase')
runner = TestRunner(suite=suite)
runner.run(count=3, interval=2)
```

**参数说明：**

- count：用来指定用例失败重运行的次数
- interval：指定每次重运行的时间间隔

