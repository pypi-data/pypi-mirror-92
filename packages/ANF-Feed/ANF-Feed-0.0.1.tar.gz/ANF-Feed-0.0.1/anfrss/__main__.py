'''
    Main of the Package

This script is importing the run function of
the GUI Module and starting it.

It is defined as an entry_point in the setup.py,
so there are two options to start this script:
    - $ python3 -m anfrss
    - $ anfrss
'''


try:
    from gui import run
except ImportError:
    from .gui import run


if __name__ == '__main__':
    run()
