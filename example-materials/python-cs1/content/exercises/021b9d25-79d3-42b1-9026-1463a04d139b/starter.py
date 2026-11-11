attendance = []

for piece in input().split():
    attendance.append(int(piece))

total = 0

for visitors in attendance:
    total = total + visitors

busy_count = 0

for visitors in attendance:
    if visitors >= 100:
        busy_count = busy_count + 1

print(f"Periods: {len(attendance)}")
print(f"Total visitors: {total}")
print(f"Busy periods: {busy_count}")
