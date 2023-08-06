"""
Python package configuration
https://packaging.python.org/tutorials/packaging-projects/

To build from source and publish to PyPI (requires the twine package):

python setup.py sdist bdist_wheel
twine upload dist/* --skip-existing
"""

import setuptools

with open('README.md') as file:
    readme = file.read()

setuptools.setup(
    name='conveyorbelt',
    version='0.0.3',
    author='Joe Heffer',
    author_email='j.heffer@sheffield.ac.uk',
    description='Command line interface for the CONVEYOR laboratory information management system (LIMS)',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/sheffield-bioinformatics-core/conveyor-belt',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests~=2.25',
        'click~=7.1',
    ],
    entry_points=dict(
        console_scripts=[
            'conveyorbelt=conveyorbelt.__main__:main'
        ]
    )
)
