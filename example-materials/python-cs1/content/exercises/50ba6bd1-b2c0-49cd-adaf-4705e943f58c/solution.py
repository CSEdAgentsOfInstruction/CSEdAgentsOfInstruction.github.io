def select_finalists(scores, minimum):
    """Return qualifying scores in a new list, preserving order and repeats.

    Return an empty list when none qualify, and do not modify scores.
    """
    finalists = []

    for score in scores:
        if score >= minimum:
            finalists.append(score)

    return finalists


def total_points(scores):
    """Return the supplied scores' total, or 0 when empty, without modifying them."""
    total = 0

    for score in scores:
        total = total + score

    return total


def print_shortlist(finalists, total):
    """Print the supplied finalist list and total on two labeled lines."""
    print(f"Finalists: {finalists}")
    print(f"Combined points: {total}")


def main():
    scores = [71, 84, 90, 84, 63]
    minimum = 84

    finalists = select_finalists(scores, minimum)
    total = total_points(finalists)
    print_shortlist(finalists, total)


main()
