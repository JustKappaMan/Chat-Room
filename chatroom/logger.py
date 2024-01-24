import logging


class Logger:
    """
    A class for creating and configuring `logging.Logger` instances.
    """

    __slots__ = ("logger",)

    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        pattern: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_to_file: bool = False,
        log_to_console: bool = True,
    ):
        """
        Create a new `logging.Logger` and configure it according to the given parameters.

        Use the `get` method to retrieve the instance after initialization.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(pattern)

        if log_to_file:
            handler = logging.FileHandler(f"{name}.log", encoding="utf-8")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if log_to_console:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get(self) -> logging.Logger:
        """
        Retrieve the custom `logging.Logger` instance.
        """
        return self.logger
