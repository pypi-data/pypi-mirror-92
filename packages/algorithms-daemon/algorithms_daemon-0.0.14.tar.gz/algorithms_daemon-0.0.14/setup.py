import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algorithms_daemon",
    packages=['algorithms_daemon'],
    package_dir={'': 'src'},
    version="0.0.14",
    author="rwecho",
    author_email="rwecho@live.com",
    description="A daemon of conriander python algorithm, communicate progress or stauts to AgentService. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "grpcio==1.31.0",
        "protobuf==3.13.0"
    ],
    python_requires='>=3.6',
)
