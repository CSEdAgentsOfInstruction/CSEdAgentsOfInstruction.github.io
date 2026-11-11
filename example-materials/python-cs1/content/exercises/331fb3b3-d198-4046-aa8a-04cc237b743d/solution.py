def total_distance(distances):
    total = 0

    for distance in distances:
        total = total + distance

    return total


def average_distance(distances):
    return total_distance(distances) / len(distances)


def count_long_stages(distances, minimum):
    count = 0

    for distance in distances:
        if distance >= minimum:
            count = count + 1

    return count


def summarize_route(distances, minimum):
    total = total_distance(distances)
    average = average_distance(distances)
    long_count = count_long_stages(distances, minimum)
    return [total, average, long_count]

