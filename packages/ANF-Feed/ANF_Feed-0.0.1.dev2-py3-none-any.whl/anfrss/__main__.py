'''
    __main__

This script is importing the run function of
the GUI Module and starting it.
'''


try:
    from gui import run
except ImportError:
    from .gui import run


if __name__ == '__main__':
    run()
