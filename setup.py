"""
Used to create a command-line tool with setup tools

-- Add path to venv into PyCharm
       - Project Settings/Project Interpreter/<right click on gear icon>
        /Show all/<click on dirtree icon>
        /<click on add icon>/
        select the path of current tools project

-- Go to command prompt, navigate to current project subfolder

-- Activate virtualenv,
>>> virtualenv venv
>>> . venv/bin/activate
>>> pip install --editable .

-- Install actual module in develop mode
>>> python setup.py develop --no-deps

-- Use on console
>>> tools --help

"""

from setuptools import setup

setup(
    name='tools',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'Click', "pyyaml", "pony", "pywin32", "setuptools"
    ],
    entry_points='''
        [console_scripts]
        tools=main:cli
    ''',
)
