"""Setup for the resumify package."""

import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Devansh Soni",
    author_email="sonidev0201@gmail.com",
    name='resumify',
    license="MIT",
    description='A Python package which uses fpdf library to create Resume.',
    version='v1.1.7',
    long_description=README,
    url='https://github.com/devansh-07/resumify',
    packages=setuptools.find_packages(),
    package_data={
            'resumify': ['fonts/Ubuntu/*.ttf'],
        },
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=['fpdf'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
