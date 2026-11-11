minutes_until_departure = int(input())

if minutes_until_departure < 30:
    print("Get ready.")
elif minutes_until_departure < 10:
    print("Leave now.")
else:
    print("Plenty of time.")
