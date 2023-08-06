import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libeasyobv",
    version="0.0.1",
    author="Qianfeng (Clark) Shen",
    author_email="qianfeng.shen@gmail.com",
    description="easyobv python3 library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QianfengClarkShen/libeasyobv",
    packages=['libeasyobv'],
    install_requires=[
        'libfpga',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.5.0',
)
