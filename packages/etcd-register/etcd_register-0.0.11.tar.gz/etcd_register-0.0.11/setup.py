from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="etcd_register",  # 包名字
    version="0.0.11",
    url="https://github.com/wuranxu/etcd_register",  # 包连接, 通常是github上的连接或readthedocs连接
    description="A register method for grpc to etcd",
    long_description=long_description,  # 将说明文件设置为README.md
    long_description_content_type="text/markdown",
    packages=find_packages(),  # 默认从当前目录下搜索包
    data_files=[
        ('', ['etcd_register/proto/invoke.proto']),
    ],
    package_data={
        '': ['*.proto'],
        'bandwidth_reporter': ['*.proto']
    },
    author="woody",
    author_email="619434176@qq.com",
    python_requires='>=3.6',
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ),
)
