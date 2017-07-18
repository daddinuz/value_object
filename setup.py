import sys
from setuptools import setup, find_packages

major, minor1, minor2, release, serial = sys.version_info
readfile_kwargs = {'encoding': 'utf-8'} if major >= 3 else {}


def readfile(filename):
    with open(filename, **readfile_kwargs) as fp:
        contents = fp.read()
    return contents


def get_packages(path):
    out = [path]
    for x in find_packages(path):
        out.append('{}/{}'.format(path, x))
    return out


packages = get_packages('value_object')
setup(
    name='value_object',
    version='0.1.0',
    description='Value Object',
    url='https://github.com/daddinuz/value_object',
    author='daddinuz',
    author_email='daddinuz@gmail.com',
    license='MIT',
    packages=packages,
    zip_safe=False,
    test_suite='value_object.test',
    keywords='value_object',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
)
