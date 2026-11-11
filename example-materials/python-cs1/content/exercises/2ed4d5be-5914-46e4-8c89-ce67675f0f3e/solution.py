# Workshop reference solution.
temperatures = []

for number in range(4):
    temperatures.append(int(input()))

lowest = temperatures[0]
for temperature in temperatures:
    if temperature < lowest:
        lowest = temperature

print(f"Lowest: {lowest}")
