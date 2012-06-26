# -*- coding: utf-8 -*-

from setuptools import setup

from hieroglyph import __version__ as version

with open('README.txt', 'r') as readme:
    long_description = readme.read()

requires = ['Sphinx>=0.6']

setup(
    name='hieroglyph',
    packages=['hieroglyph'],
    version = "{version}".format(version=version),
    url='http://code.google.com/p/hieroglyph/',
    download_url="http://code.google.com/p/hieroglyph/downloads/detail?name=hieroglyph-{version}.tar.gz".format(version=version),
    license='BSD',
    author='Robert Smallshire',
    author_email='robert@smallshire.org.uk',
    description='Sphinx "hieroglyph" extension',
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
