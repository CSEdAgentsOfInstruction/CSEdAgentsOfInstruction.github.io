# Workshop reference solution.
count = int(input())
energy_levels = []

for number in range(count):
    energy_levels.append(int(input()))

for index in range(len(energy_levels)):
    if energy_levels[index] < 0:
        energy_levels[index] = 0

print(energy_levels)
