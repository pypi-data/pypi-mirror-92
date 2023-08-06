import setuptools



setuptools.setup(
    name="multipolygon", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.1", # 版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="李厚奇", # 作者
    author_email="884359533@qq.com", #邮箱
    description="判断某个坐标点[x,y]是否在一个多边形内[[x,y],[x,y],[x,y],[x,y]]", # 描述
    long_description='判断某个坐标点[x,y]是否在一个多边形内[[x,y],[x,y],[x,y],[x,y]],每个ｘ,y坐标点都需要写入到一个列表中', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://github.com/tanxinyue/isin_multipolygon", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',  #支持python版本
)
