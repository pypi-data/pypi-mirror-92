"""Moon coverage setup."""

import re

from setuptools import setup, find_packages


with open('moon_coverage/version.py') as f:
    __version__ = re.findall(
        r'__version__ = \'(\d+\.\d+\.\d+)\'',
        f.read()
    )[0]


setup(
    name='moon-coverage',
    version=__version__,
    description='Moon Coverage toolbox',
    author='Benoit Seignovert, Rozenn Robidel',
    author_email='benoit.seignovert@univ-nantes.fr',
    url='https://gitlab.univ-nantes.fr/esa-juice/moon-coverage',
    license='BSD',
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19',
        'matplotlib>=3.3',
        'spiceypy>=3.1',
        'Pillow>=8.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['moon', 'coverage', 'esa', 'juice'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
)
