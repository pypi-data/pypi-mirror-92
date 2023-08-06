#!/usr/bin/env python
#/* *=+=+=+=+* *** *=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#  * 文档信息: *** :~/WORKM/studyCode/pythonCode/pipInstallExample/gsc_package/setup.py
#  * 版权声明: *** :(魎魍魅魑)MIT
#  * 联络信箱: *** :guochaoxxl@163.com
#  * 创建时间: *** :2021年01月27日的下午08:23
#  * 文档用途: *** :Python趣味编程入门与实战
#  * 作者信息: *** :guochaoxxl(http://cnblogs.com/guochaoxxl)
#  * 修订时间: *** :2021年第04周 01月27日 星期三 下午08:23 (第027天)
#  * 文件描述: *** :自行添加
# * *+=+=+=+=* *** *+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+*/
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="xxlGsc",
        version="0.01",
        author="GSC",
        author_email="guochaoxxl@163.com",
        description="xing xiu lao xian, fa li wu bian!",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/guochaoxxl/learnPython",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)
