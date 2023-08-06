from setuptools import setup

setup(
    name='LifeGame',
    version='1.0.0',
    description='Conway\'s Game of Life in Python.',
    url='https://github.com/Oscarozo/GameofLife',
    author='Oscar Ozorio',
    author_email='osvaldo15963@fpuna.edu.py',
    license='GPL-3.0',
    packages=['GameofLife'],
    scripts=[
        'bin/GameofLife',
        'bin/GameofLife.bat'
    ],
    zip_safe=False,
    install_requires=['pygame']
)
