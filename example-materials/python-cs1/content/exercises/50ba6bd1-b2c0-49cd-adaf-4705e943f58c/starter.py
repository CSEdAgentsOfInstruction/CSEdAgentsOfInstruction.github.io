def select_finalists(scores, minimum):
    return []


def total_points(scores):
    return 0


def print_shortlist(finalists, total):
    print("Finalists: []")
    print("Combined points: 0")


def main():
    scores = [71, 84, 90, 84, 63]
    minimum = 84

    finalists = select_finalists(scores, minimum)
    total = total_points(finalists)
    print_shortlist(finalists, total)


main()
