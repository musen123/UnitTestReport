"""
============================
Author:柠檬班-木森
Time:2020/7/16   16:20
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
from setuptools import setup, find_packages

with open("readme.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='unittestreport',
    version='1.1.12',
    author='MuSen',
    author_email='musen_nmb@qq.com',
    url='https://github.com/musen123/UnitTestReport',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Jinja2==2.10.1", "PyYAML==5.3.1","requests==2.24.0"],
    packages=find_packages(),
    package_data={
        "": ["*.html"],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
