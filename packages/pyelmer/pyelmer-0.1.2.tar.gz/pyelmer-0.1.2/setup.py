# https://packaging.python.org/tutorials/packaging-projects/

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyelmer',  
    version='0.1.2',
    author='Arved Enders-Seidlitz',
    author_email='arved.enders-seidlitz@ikz-berlin.de',
    description='A python interface to Elmer.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nemocrys/pyelmer',
    packages=['pyelmer', 'pyelmer.test'],
    include_package_data=True,
    package_data={'': ['data/*.yml']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    install_requires=[
      #'Django >= 1.1.1',
      'gmsh',
      'pyyaml',
      'matplotlib',
    ],
    python_requires='>=3.7',
 )
