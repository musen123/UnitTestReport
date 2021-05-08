"""
============================
Author:柠檬班-木森
Time:2020/8/19   17:33
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

import traceback
import time


def run_count(count, interval, func, *args, **kwargs):
    """运行计数"""
    for i in range(count):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("====用例执行失败===")
            traceback.print_exc()
            if i + 1 == count:
                raise e
            else:
                print("==============开始第{}次重运行=============".format(i))
                time.sleep(interval)
        else:
            break


def rerun(count, interval=2):
    """
    单个测试用例重运行的装饰器,注意点，如果使用了ddt,那么该方法要在用在ddt之前
    :param count: 失败重运行次数
    :param interval: 每次重运行间隔时间,默认三秒钟
    :return:
    """

    def wrapper(func):
        def decorator(*args, **kwargs):
            run_count(count, interval, func, *args, **kwargs)
        return decorator

    return wrapper


