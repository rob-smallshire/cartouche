# -*- coding: utf-8 -*-

from setuptools import setup

version = '1.1.1'

with open('README.txt', 'r') as readme:
    long_description = readme.read()

requires = ['Sphinx>=0.6']

setup(
    name='cartouche',
    packages=['cartouche'],
    version = "{version}".format(version=version),
    url='https://github.com/rob-smallshire/cartouche',
    download_url="https://pypi.python.org/pypi/cartouche",
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
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    #packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    requires=['sphinx'],
)
