# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.txt', 'r') as readme_file:
    readme = readme_file.read()

requires = ['Sphinx>=0.6']

setup(
    name='hieroglyph',
    version='0.5',
    url='http://code.google.com/p/hieroglyph/',
    download_url='http://pypi.python.org/pypi/hieroglyph',
    license='BSD',
    author='Robert Smallshire',
    author_email='robert@smallshire.org.uk',
    description='Sphinx "hieroglyph" extension',
    long_description=readme,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)