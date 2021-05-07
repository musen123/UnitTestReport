# 

关于测试用例预期结果和实际结果的比对的,apin中封装了一个verification字段，只需要在verification中定义预期结果，实际结果提取表达式，和断言的方法，即可实现用例的断言！

### 1、基本语法

```python
verification = [
        [断言方式, 预期结果, 实际结果]
    ] 
```

### 2、断言方式

apin中目前支持两种断言方式：

**1、断言相等 ：eq**

预期结果和实际结果相等

```python
verification = [
        ['eq', 预期结果, 实际结果]
    ] 
```

**2、断言包含：contians**



实际结果中包含预期结果的内容

```python
verification = [
        ['contians', 预期结果, 实际结果]
    ] 
```

### 3、实际结果获取

​	关于断言的实际结果提取，需要使用`V{{表达式}}`来进行提取，表达式支持jsonpath和正则表达式两种提取方式方式。

**3.1、正则表达式提取**

```python
# 通过正则表达式来提取实际结果中的msg字段。
verification = [
        ['contians', {'msg':"OK"}, {"msg": "V{{msg:'(.+?)'}}"}]
    ] 

```

**3.2、通过jsonpath提取**

```python
# 通过jsonpath来提取实际结果中的msg字段。
verification = [
        ['contians', {'msg':"OK"}, {"msg": 'V{{$..msg}}']
    ] 

```



### 4、HTTP状态码的断言

​	上述两种方式，以可提取结果返回的数据，那如果要断言接口http请求的状态码呢？apin中也提供了一个内置的字段名`status_code`，来表示http状态码

```python
# 断言接口请求的http状态码是否等于200
verification = [
        ['eq', 200, 'status_code']
    ] 
```

