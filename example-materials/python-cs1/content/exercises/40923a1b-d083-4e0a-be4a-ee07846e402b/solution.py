# Workshop reference solution.
count = int(input())
values = []

for number in range(count):
    values.append(int(input()))

expanded_values = []

for index in range(len(values)):
    expanded_values.append(values[index])
    expanded_values.append(values[index] * 2)

print(f"Original: {values}")
print(f"Expanded: {expanded_values}")
