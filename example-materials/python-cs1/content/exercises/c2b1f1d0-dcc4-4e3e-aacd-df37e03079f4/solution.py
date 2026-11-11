minutes_until_departure = int(input())

if minutes_until_departure < 10:
    print("Leave now.")
elif minutes_until_departure < 30:
    print("Get ready.")
else:
    print("Plenty of time.")
