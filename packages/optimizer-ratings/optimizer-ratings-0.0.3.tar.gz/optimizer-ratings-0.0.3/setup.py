import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="optimizer-ratings",
    version="0.0.3",
    description="Compares performance of optimizers used for time series model hyper-param optimization",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/optimizer-ratings",
    author="microprediction",
    author_email="pcotton@intechinvestments.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["optimizer-ratings"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["wheel","pathlib","numpy>=1.16.5","timemachines","pytest","microprediction"],
)
