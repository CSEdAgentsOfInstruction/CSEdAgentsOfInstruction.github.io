def triple(number):
    return number * 3


def check_triple():
    assert triple(2) == 6
    assert triple(0) == 0
    assert triple(-5) == -15


check_triple()
