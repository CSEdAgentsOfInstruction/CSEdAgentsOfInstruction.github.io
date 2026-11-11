# Keeping the total and busy-period count separate lets us test each calculation.
def total_attendance(attendance):
    total = 0

    for visitors in attendance:
        total = total + visitors

    return total


def count_busy_periods(attendance, minimum):
    count = 0

    for visitors in attendance:
        if visitors >= minimum:
            count = count + 1

    return count


def attendance_summary(attendance, minimum):
    total = total_attendance(attendance)
    busy_count = count_busy_periods(attendance, minimum)
    return [len(attendance), total, busy_count]


def main():
    attendance = []

    for piece in input().split():
        attendance.append(int(piece))

    summary = attendance_summary(attendance, 100)
    print(f"Periods: {summary[0]}")
    print(f"Total visitors: {summary[1]}")
    print(f"Busy periods: {summary[2]}")


main()
