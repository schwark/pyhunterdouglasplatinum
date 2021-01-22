# pyhunterdouglasplatinum
Hunter Douglas Platinum Control

Python library to control shades via the Hunter Douglas Platinum hub.

## Installation

You can install the Real Python Feed Reader from [PyPI](https://pypi.org/project/pyhunterdouglasplatinum/):

    pip install pyhunterdouglasplatinum

The module is supported on Python 2.7, as well as Python 3.4 and above.

## How to use

The module can also be used at the command line using

    python -m hunterdouglasplatinum <params>

The paramters that the command line tool takes are in the available via --help

```
❯ python -m hunterdouglasplatinum --help
usage: hunterdouglasplatinum [-h] [-d SHADE] [-n SCENE] [-l LEVEL] ip

positional arguments:
  ip                    ip address of the hub

optional arguments:
  -h, --help            show this help message and exit
  -d SHADE, --shade SHADE
                        name of the shade
  -n SCENE, --scene SCENE
                        name of the scene
  -l LEVEL, --level LEVEL
                        level of the shade <up/down/percentage>
```

## Library commands

The library documentation (somewhat) is here - [pdoc](https://github.com/schwark/pyhunterdouglasplatinum/blob/main/docs/hunterdouglasplatinum/hunterdouglasplatinum.md)