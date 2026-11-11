def with_reading_added(readings, reading):
    extended = []

    for value in readings:
        extended.append(value)

    extended.append(reading)
    return extended
