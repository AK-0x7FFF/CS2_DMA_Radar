from logging import DEBUG, getLogger, StreamHandler, ERROR, WARNING, INFO, Formatter, Logger


def logger_setup() -> Logger:
    class ColoredFormatter(Formatter):
        def format(self, record):
            record.levelname = {
                DEBUG: f'\033[95m[{record.levelname}]\033[0m',
                INFO: f'\033[92m[{record.levelname}]\033[0m',
                WARNING: f'\033[93m[{record.levelname}]\033[0m',
                ERROR: f'\033[91m[{record.levelname}]\033[0m',
            }.get(record.levelno, record.levelname)

            return super().format(record)

    handler = StreamHandler()
    handler.setFormatter(ColoredFormatter(" ".join((
        "%(levelname)s",
        # "\033[1;32m[%(asctime)s]\033[0m",
        # "\033[1;35m[%(filename)s:%(lineno)s]\033[0m",
        # "\033[1;35m[%(filename)s]\033[0m",
        "\033[1;97m%(message)s\033[0m",
    ))))

    logger = getLogger()
    logger.addHandler(handler)
    logger.setLevel(DEBUG)

    [logger.info(line) for line in r"""  /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$$$
 /$$__  $$| $$  /$$/ /$$__  $$ /$$__  $$|_____ $$//$$__  $$|_____ $$/
| $$  \ $$| $$ /$$/ |__/  \ $$|__/  \ $$     /$$/| $$  \__/     /$$/ 
| $$$$$$$$| $$$$$/     /$$$$$/  /$$$$$$/    /$$/ | $$$$$$$     /$$/  
| $$__  $$| $$  $$    |___  $$ /$$____/    /$$/  | $$__  $$   /$$/   
| $$  | $$| $$\  $$  /$$  \ $$| $$        /$$/   | $$  \ $$  /$$/    
| $$  | $$| $$ \  $$|  $$$$$$/| $$$$$$$$ /$$/    |  $$$$$$/ /$$/     
|__/  |__/|__/  \__/ \______/ |________/|__/      \______/ |__/""".split("\n")]

    return logger