from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='vk-spammer',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts':
            ['vk-spammer=core.spam:main']
    },
    install_requires=[
        'vk'
    ]
)