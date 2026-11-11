def replace_negative_readings(values):
    for index in range(len(values)):
        if values[index] < 0:
            values[index] = 0

