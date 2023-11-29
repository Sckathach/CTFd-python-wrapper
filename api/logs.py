from api import SIMPLE_VERBOSE, FULL_VERBOSE


def log(log_type, message):
    if log_type == "SIMPLE" and SIMPLE_VERBOSE:
        print("-- " + message)
    elif log_type == "FULL" and FULL_VERBOSE:
        print("-- " + message)
    elif log_type == "ANYWAY":
        print("-- -" + message)
