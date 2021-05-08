# 

### 1、使用介绍

关于数据驱动这边就不给大家做过多的介绍了，数据驱动的目的是将测试数据和用例逻辑进行分离，提高代码的重用率，以及用例的维护，关于数据驱动本，unittestreport.dataDriver模块中实现了三个使用方法，支持使用列表(可迭代对象)、json文件、yaml文件来生成测试用例，接来分别给大家介绍一下使用方法：

```
from unittestreport.dataDriver import ddt, list_data,json_data,yaml_data
```

- **第一步：使用ddt装饰测试用例类**

- **第二步：根据数据存储的方式，选择对应的方法进行传入用例数据**

### 2、list_data的使用

用例数据保存在可迭代对象中（如列表），则可以使用list_data来实现数据

```python
from unittestreport import ddt, list_data
@ddt
class TestClass(unittest.TestCase):
    cases = [{'title': '用例1', 'data': '用例参数', 'expected': '预期结果'}, 
             {'title': '用例2', 'data': '用例参数', 'expected': '预期结果'},
             {'title': '用例3', 'data': '用例参数', 'expected': '预期结果'}]
    @list_data(cases)
    def test_case(self, data):
        pass

```

> **用例数据的格式:列表嵌套字典**





### 3、json_data

用例保存在json文件中，则可以使用json_data来实现数据驱动，使用json_data时，直接传入json文件的路径即可

```python
from unittestreport import ddt,json_data

@ddt
class TestClass(unittest.TestCase):
    @json_data('C:/xxx/xxx.json')
    def test_case(self, data):
        pass

```

json文件中的数据格式如下：

```json
[
  {
    "title": "用例1",
    "data": "用例参数",
    "expected": "预期结果"
  },
  {
    "title": "用例2",
    "data": "用例参数",
    "expected": "预期结果"
  },
  {
    "title": "用例3",
    "data": "用例参数",
    "expected": "预期结果"
  }
]

```

### 4、yaml_data

用例保存在json文件中，则可以使用json_data来实现数据驱动，使用json_data时，直接传入json文件的路径即可

```python
from unittestreport import ddt,yaml_data

@ddt
class TestClass(unittest.TestCase):
    @yaml_data("C:/xxxx/xxx/cases.yaml")
    def test_case(self, data):
        pass

```

yaml文件中的数据展示

```yaml
- title: 用例1
  data: 用例参数
  expected: 预期结果

- title: 用例2
  data: 用例参数
  expected: 预期结果
  
- title: 用例4
  data: 用例参数
  expected: 预期结果

```

### 5、注意点：

- 关于使用ddt的时候进行数据驱动，指定测试报告中的用例描述：

- 测试报告中的用例描述默认使用的是用例方法的文档字符串注释，
- 如果要给每一条用例添加用例描述，需要在用例数据中添加title或者desc字段，字段对应的数据会自动设置为测试报告中用例的描述

![image](..\img\1620456435887.png)



