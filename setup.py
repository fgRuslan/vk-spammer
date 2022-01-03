from setuptools import setup, find_packages
from os.path import join, dirname

long_description = open('README.md').read()

DESCRIPTION = 'Спаммер для ВК'
LONG_DESC = long_description

setup(
    name='vk-spammer',
    version='1.2.3.9',
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
        'vk_api',
        'python3-anticaptcha',
        'requests'
    ]
)
