def has_access_code(codes, required_code):
    for code in codes:
        if code == required_code:
            return True

    return False


def check_access_codes():
    assert has_access_code(["A7", "B4"], "A7") == True
    assert has_access_code(["A7", "B4", "C9"], "B4") == True
    assert has_access_code(["A7", "B4"], "X2") == False
    assert has_access_code([], "A7") == False


check_access_codes()
