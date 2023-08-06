import setuptools

desc_file = "README.md"

with open(desc_file, "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webapitest",
    version="0.1.3",
    author="Huangyan",
    author_email="345471536@qq.com",
    description="Testing tool for web api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/wow_1/webapitest",
    keywords=["web", "api", "test", "postman"],
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    python_requires=">=3.3",
    license="MIT",
entry_points={'console_scripts': ['webapitest = webapitest.main:main']},
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    data_files=[desc_file],
)