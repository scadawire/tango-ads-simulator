import setuptools

setuptools.setup(
    name="tango-ads-simulator",
    version="0.1.0",
    author="Sebastian Jennen",
    author_email="sj@imagearts.de",
    description="tango-ads-simulator device driver",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['requests'],
    scripts=['AdsSimulator.py']
)