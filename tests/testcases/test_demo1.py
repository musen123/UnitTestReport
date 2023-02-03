from functools import wraps
import unittest


def data(*args):
    def wrapper(func):
        setattr(func, "PARAMS", args)
        return func

    return wrapper


def update_test_func(test_func, case_data):
    @wraps(test_func)
    def wrapper(self):
        return test_func(self, case_data)

    return wrapper


def ddt(cls):
    for name, func in list(cls.__dict__.items()):
        if hasattr(func, "PARAMS"):
            for index, case_data in enumerate(getattr(func, "PARAMS")):
                # 生成一个用例方法名
                new_test_name = "{}_{}".format(name, index)
                # 修改原有的测试方法，设置用例数据为测试方法的参数
                test_func = update_test_func(func, case_data)
                setattr(cls, new_test_name, test_func)
            else:
                delattr(cls, name)
    return cls


@ddt
class TestDome(unittest.TestCase):
    @data([{'title':'musen01'}])
    def test_demo(self, data):
        assert 1==2

    @data([{'title': 'musen01'}],{'title': 'musen01'})
    def test_demo2(self, data):
        assert 1 == 1