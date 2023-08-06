from setuptools import setup
import os

readme_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.rst')

def readme_contents():
    with open(readme_dir) as readme:
        file_contents = readme.read()

    return file_contents
setup(
    name='LifeGame',
    version='1.0.2',
    description='Conway\'s Game of Life in Python.',
    long_description=readme_contents(),
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
