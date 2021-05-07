# 

apin支持在测试用例中调用自定义的函数来处理数据，如对数据进行加密处理、随机生成数据等等。

#### 1、自定义函数

apin创建的项目中有一个funcTools.py，在该文件中可以自己定义函数，然后在用例中通过F{xxx()}来调用。

- **案例：funcTools.py文件**

```python
import hashlib,random

def md5_encrypt(msg):
    """md5加密"""
    md5 = hashlib.md5()  
    md5.update(msg.encode("utf8"))  
    return md5.hexdigest()

def rand_phone():
	"""随机生成手机号的函数"""
    import random
    for i in range(8):
        phone += str(random.randint(0, 9))
    return str(phone)


def get_timestamp():
    """获取时间戳"""
    return time.time()

```

- **注意点：函数处理完的数据需要return返回哦**

### 2、用例中引用函数

- **引用表达式：F{函数名()}**

    用例数据中的user，引用前面定义的rand_phone函数

```python
{
	'title': "普通用户注册",
	'interface': "member/register",
	"method": "post",
	'json': {"user": "F{rand_phone()}", "pwd": "lemon123"},
}
```

用例数据中的pwd，引用前面定义的md5_encrypt函数对密码进行md加密

- **注意点：引用的函数，传递的参数如果是变量，则不需要在变量应用表达式外加引号**

```python
{
	'title': "普通用户登录",
	'interface': "member/login",
	"method": "post",
	'json': {"user": "13109877890", "pwd": "F{md5_encrypt('lemon123')}"},
}

# 引用函数，变量作为参数传递
{
	'title': "普通用户登录",
	'interface': "member/login",
	"method": "post",
	'json': {"user": "${{user}}", "pwd": "F{md5_encrypt(${{pwd}})}"},
}
```

