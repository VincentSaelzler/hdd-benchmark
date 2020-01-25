def is_prod():
    # use this for real systems where you actually want to test (INCL WIPING) the disks
    # return True
    # use this when testing in dev environments.
    return False


def enable_run_badblocks():
    # use this for real systems where you actually want to test (INCL WIPING) the disks
    return True
    # use this when testing in dev environments.
    # return False
