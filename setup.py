# encoding: utf-8
from codecs import open  # to use a consistent encoding
from setuptools import setup, find_packages
from subprocess import check_output
from os import environ, path

here = path.abspath(path.dirname(__file__))

if path.exists(path.join(here, "version.sh")):  # development
    if 'PYTHON_PACKAGE_VERSION' in environ:
        version = environ['PYTHON_PACKAGE_VERSION']
    else:
        version = check_output(path.join(here, "version.sh")).strip()
    package_name = path.basename(here)
else:  # source package
    with open(path.join(here, "PKG-INFO")) as f:
        for line in f.readlines():
            if line.startswith("Version:"):
                version = line.split(":")[1].strip()
            elif line.startswith("Name:"):
                package_name = line.split(":")[1].strip()
package = package_name.replace('-', '_')

setup(
    name=package_name,
    version=version,
    description='Sauce Labs Storage API library and command-line tool',
    url='https://github.com/saucelabs/{}'.format(package_name),
    author='Sauce Labs',
    author_email='dev@saucelabs.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords=['saucelabs'],
    packages=find_packages(),
    install_requires=[],
    package_data={
        package: ['version.json'],
    },
    scripts=["bin/saucestorage"]
)
