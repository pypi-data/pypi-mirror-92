import os
from setuptools import find_packages, setup
import json

PROJECT_DIR = os.path.dirname(__file__)

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('./package.json') as package:
    data = json.load(package)
    version = data['version']

setup(
    name='django_namek',
    version=version,
    url='https://github.com/Aleksi44/django-namek',
    author="Alexis Le Baron",
    author_email="hello@snoweb.fr",
    description="Django app for forms chaining with some features",
    long_description=long_description,
    keywords="django forms session namek",
    license='GPL-3.0',
    install_requires=[
        'django>=3.1.1',
        'selenium>=3.141.0',
        'pyvirtualdisplay>=0.2.5',
        'Faker>=4.14.0',
        'webdriver-manager>=3.2.2'
    ],
    platforms=['linux'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ]
)
