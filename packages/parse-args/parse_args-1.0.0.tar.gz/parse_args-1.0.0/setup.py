print('Pixelsuft Parse Arguments')
from setuptools import setup as setup_tools_setup
from setuptools import find_packages as setup_tools_find_packages


long_description = '''# Pixelsuft Parse Arguments
Parse Command Line Arguments From String
# Example
```
from parse_args import get as get_args
print(str(get_args('   test.exe /f /m --file "lol lol.txt" --test 1 2')))
```
Output:<br />
['test.exe', '/f', '/m', '--file', 'lol lol.txt', '--test', '1', '2']
'''

setup_tools_setup(
    name="parse_args",
    version="1.0.0",
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