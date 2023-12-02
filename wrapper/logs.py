SIMPLE_VERBOSE = True
FULL_VERBOSE = False


def log(log_type, message):
    if log_type == "SIMPLE" and SIMPLE_VERBOSE:
        print("-- " + message)
    elif log_type == "FULL" and FULL_VERBOSE:
        print("-- " + message)
    elif log_type == "ANYWAY":
        print("-- -" + message)
