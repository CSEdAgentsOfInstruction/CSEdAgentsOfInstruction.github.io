count = int(input())
temperatures = []

for number in range(count):
    temperatures.append(int(input()))

for temperature in temperatures:
    if temperature >= 20:
        print(temperature)
