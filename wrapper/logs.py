class Log:
    def __init__(self, from_):
        self.from_: str = from_
        self.level: int = 1

    def info(self, message: str):
        if self.level >= 2:
            print(f"-- INFO: {message}")

    def warning(self, message: str):
        if self.level >= 2:
            print(f"-- WARNING: {message}")

    def error(self, message: str):
        if self.level >= 1:
            print(f"-- ERROR: ({self.from_}) {message}")

    def debug(self, message: str):
        if self.level >= 3:
            print(f"-- DEBUG: ({self.from_}) {message}")
