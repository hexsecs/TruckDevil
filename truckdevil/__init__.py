name = "truckdevil"
__version__ = "1.2.0"


def main(argv=None):
    from .truckdevil import main as cli_main

    return cli_main(argv)
