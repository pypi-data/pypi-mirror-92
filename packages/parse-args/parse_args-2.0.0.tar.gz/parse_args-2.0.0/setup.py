print('Pixelsuft Parse Arguments')
from setuptools import setup as setup_tools_setup
from setuptools import find_packages as setup_tools_find_packages


long_description = '''# Pixelsuft Parse Arguments
Parse Command Line Arguments From String
# Change Log
Added ```set``` Function For Getting String From Arguments
# Example
```
from parse_args import get as get_args
from parse_args import set as get_str
print(str(get_args('   test.exe /f /m --file "lol lol.txt"   --test 1 2')))
print(get_str(['test.exe', '-F', 'test.txt lol']))
```
Output:<br />
['test.exe', '/f', '/m', '--file', 'lol lol.txt', '--test', '1', '2']<br />
"test.exe" "-F" "test.txt lol"
'''

setup_tools_setup(
    name="parse_args",
    version="2.0.0",
    author="Pixelsuft",
    description="Parse Command Line Arguments From String",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setup_tools_find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.5',
    license='MIT', 
    keywords='parse_args',
    install_requires=[''],
    py_modules=["parse_args"]
)