battery_percentage = int(input())

if battery_percentage < 20:
    print("Low battery")
elif battery_percentage < 80:
    print("Battery okay")
else:
    print("Battery high")
