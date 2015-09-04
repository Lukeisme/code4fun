from setuptools import setup, find_packages

setup(
    name='xueqiu',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = xueqiu.settings']},
)
