def has_access_code(codes, required_code):
    for code in codes:
        if code == required_code:
            return True
        else:
            return False


def check_access_codes():
    assert has_access_code(["A7", "B4"], "A7") == True
    # Add checks based on the required behavior.


check_access_codes()
