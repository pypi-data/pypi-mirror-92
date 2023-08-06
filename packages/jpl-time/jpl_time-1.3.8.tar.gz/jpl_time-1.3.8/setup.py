from setuptools import setup
import sys

if sys.version_info.major < 3:
    install_requires = [
        'setuptools==38.0.0',
        'certifi<=2020.04.05.1',
        'pytz<=2020.1',
        'wheel==0.34.2',
        'numpy==1.16.4',
        'spiceypy==2.3.2'
    ],
else:
    install_requires = [
        'nose',
        'tornado',
        'setuptools',
        'six',
        'certifi',
        'pytz',
        'wheel',
        'numpy',
        'spiceypy'
    ],

setup(
    name='jpl_time',
    version='1.3.8',
    packages=['jpl_time', 'jpl_time.jpl_time_utilities'],
    url='https://github.jpl.nasa.gov/M20-Surface-Ops-Tools/jpl_time',
    license='JPL',
    author='Forrest Ridenhour',
    author_email='Forrest.Ridenhour@jpl.nasa.gov',
    description='Time and Duration classes which use SPICE to perform conversions and math.',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'jpl_time = jpl_time.jpl_time:main'
        ]
    }
)
