# -*- coding: utf-8 -*-

from setuptools import setup

from cartouche import __version__ as version

with open('README.txt', 'r') as readme:
    long_description = readme.read()

requires = ['Sphinx>=0.6']

setup(
    name='cartouche',
    packages=['cartouche'],
    version = "{version}".format(version=version),
    url='http://code.google.com/p/cartouche/',
    download_url="http://code.google.com/p/cartouche/downloads/detail?name=cartouche-{version}.zip".format(version=version),
    license='BSD',
    author='Robert Smallshire',
    author_email='robert@smallshire.org.uk',
    description='Sphinx "cartouche" extension',
    long_description=long_description,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    #packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    requires=['sphinx'],
)
