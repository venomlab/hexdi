import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hexdi',
    version='0.2.1',
    packages=find_packages(include=('hexdi',)),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.5,<4',
    url='https://github.com/zibertscrem/hexdi',
    license='MIT',
    author='Dmitriy Selischev',
    author_email='zibertscrem@gmail.com',
    description='Highly extensible Dependency injection framework for humans',
    long_description=long_description,
    install_requires=['typing']
)
