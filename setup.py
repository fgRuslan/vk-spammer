from setuptools import setup, find_packages
from os.path import join, dirname

DESCRIPTION = 'A VK spammer'
LONG_DESC = DESCRIPTION

try:
    with open("README.md", encoding="utf-8") as f:
        LONG_DESC = "\n" + f.read()
except FileNotFoundError:
    LONG_DESC = DESCRIPTION

setup(
    name='vk-spammer',
    version='1.01',
    author='fgRuslan',
    author_email='ubijca16@gmail.com',
    url='https://github.com/fgRuslan/vk-spammer',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    long_description=LONG_DESC,
    entry_points={
        'console_scripts':
            ['vk-spammer=core.spam:main']
    },
    install_requires=[
        'vk'
    ]
)