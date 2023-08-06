# _*_ coding: utf-8 _*_
"""
    @author: Jibao Wang
    @time: 2021/1/25 16:58
"""
from os import path
from codecs import open
from setuptools import setup


bashdir = path.abspath(path.dirname(__file__))
# get the long description from the README file
with open(path.join(bashdir, 'README.md'), encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='spring371327',  # 包名称
    version='0.1.0',
    url='https://github.com/wangjibao1995/FLASK-SHARE',
    license='MIT',
    author='Jibao Wang',
    author_email='wangjibao@iie.ac.cn',
    description='create social share component in Jinja2 template based on share.js',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    packages=['flask_share'],   # 要包含的包名，安装后 from flask_share import ***
    zip_safe=False,
    test_suite='test_flask_share',
    include_package_data=True,
    install_requires=['Flask'],
    keywords='flask extension development',
    classifiers=[
        'Development status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

