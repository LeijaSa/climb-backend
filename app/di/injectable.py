from kink import di


def injectable(cls):
    di[cls] = lambda di: cls()
    return cls
