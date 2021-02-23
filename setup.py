#!/usr/bin/env python
from setuptools import find_packages, setup

from django_frontify import __version__


REQUIREMENTS = []


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    # 'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Framework :: Django',
    'Framework :: Django :: 2.2',
    'Framework :: Django CMS',
    'Framework :: Django CMS :: 3.7',
]

setup(
    name='django-frontify',
    version=__version__,
    author='LAB360 GmbH',
    author_email='info@lab360.ch',
    url='https://github.com/lab360-ch/django-frontify',
    license='BSD',
    description='',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['preview']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)
