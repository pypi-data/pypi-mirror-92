import os

from setuptools import find_packages, setup

import nacos

with open(os.path.join(os.path.dirname(__file__), 'README.md'), "r", encoding='utf-8') as fh:
    LONG_DESCRIPTION = fh.read()

DESCRIPTION = (
    'Python3 client for Nacos.'
)
CLASSIFIERS = [
    'Programming Language :: Python',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    'Programming Language :: Python :: 3.6',
]
KEYWORDS = [
    'nacos', 'python-nacos', 'pynacos', 'pynacos-sdk'
]

setup(
    name='python-nacos',
    version=nacos.__version__,
    maintainer='Murray',
    maintainer_email='sunglowrise@qq.com',
    url='https://github.com/sunglowrise/python-nacos/',
    download_url='https://github.com/sunglowrise/python-nacos/',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license='MIT',
    platforms='Platform Independent',
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=["test"]),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'requests>=2.22.0'
    ],
)
