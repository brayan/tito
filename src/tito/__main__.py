from tito.utils.logger import setup_logger
setup_logger()

from tito.app import main

if __name__ == "__main__":
    main().main_loop()
