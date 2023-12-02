class Log:
    def __init__(self, from_):
        self.minimal: bool = True
        self.simple: bool = True
        self.full: bool = False
        self.from_: str = from_

    def info(self, message: str):
        if self.simple:
            print(f"-- INFO: {message}")

    def warning(self, message: str):
        if self.simple:
            print(f"-- WARNING: {message}")

    def error(self, message: str):
        if self.minimal:
            print(f"-- ERROR: ({self.from_}) {message}")

    def debug(self, message: str):
        if self.full:
            print(f"-- DEBUG: ({self.from_}) {message}")
