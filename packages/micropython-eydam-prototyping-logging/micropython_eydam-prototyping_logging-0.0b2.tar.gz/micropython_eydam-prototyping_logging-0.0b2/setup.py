import setuptools
import sdist_upip

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micropython_eydam-prototyping_logging",
    version="0.0b2",
    author="Tobias Eydam",
    author_email="eydam-prototyping@outlook.com",
    description="Some logging functions for MicroPython in combination with syslog-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eydam-prototyping/tutorials_de/blob/master/micropython/packages/ep_logging",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    #cmdclass={'sdist': sdist_upip.sdist},
    py_modules=['ep_logging']
)