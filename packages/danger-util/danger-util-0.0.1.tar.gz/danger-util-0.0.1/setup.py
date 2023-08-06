import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="danger-util",
    version="0.0.1",
    author="wushiyong",
    author_email="wushiyong1209@gmail.com",
    description="A python tool package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danger812/danger",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    'License :: OSI Approved :: Apache Software License',
    "Operating System :: OS Independent",
    ],
    install_requires = [
        'pydatahub >= 2.17.0',
        'aliyun-log-python-sdk >= 0.6.48.9',
        'mysqlclient == 1.4.6',
        'DBUtils == 1.3',
        'pexpect == 4.8.0'
    ]
)