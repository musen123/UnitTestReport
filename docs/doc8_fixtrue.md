# 

关于测试用例执行的前后置，apin中提供了四个字段来指定用例前后置执行的函数。

#### 1、setup_hook 

指定用例  的前置执行函数

```python
# 设置一个用例级别的前置函数，将前置函数的返回值，保存到局部变量的timestamp
setup_hook = {"timestamp": 'F{get_timestamp()}'}
```



#### 2、setup_class_hook

指定用例集  的前置执行函数

```python
# 设置一个测试集级别的前置函数，将前置函数的返回值，保存到局部变量的timestamp
setup_class_hook = {"timestamp": 'F{get_timestamp()}'}
```

####  3、teardown_hook

指定用例 的后置执行函数

```python
# 设置一个用例级别的后置
teardown_hook = {"teardowm": 'F{data_clear()}'}
```

####  4、teardown_class_hook

指定用例集的后置执行函数

```python
# 设置一个测试集级别的后置方法
teardown_hook = {"teardowm": 'F{data_clear()}'}
```

