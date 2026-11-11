readings = []

while True:
    reading = float(input())

    if reading == 9999:
        break

    readings.append(reading)

valid_readings = []

for reading in readings:
    if reading >= 0:
        valid_readings.append(reading)

total = 0

for reading in valid_readings:
    total = total + reading

if len(valid_readings) == 0:
    average = "none"
else:
    average = total / len(valid_readings)

print(f"Measurements entered: {len(readings)}")
print(f"Valid readings: {len(valid_readings)}")
print(f"Total rainfall: {total}")
print(f"Average rainfall: {average}")
