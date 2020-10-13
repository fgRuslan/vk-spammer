from setuptools import setup, find_packages
from os.path import join, dirname

DESCRIPTION = 'A VK spammer'

try:
    with open("README.md", encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name='vk-spammer',
    version='1.01',
    author='fgRuslan',
    author_email='ubijca16@gmail.com',
    url='https://github.com/fgRuslan/vk-spammer',
    long_description_content_type="text/markdown",
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