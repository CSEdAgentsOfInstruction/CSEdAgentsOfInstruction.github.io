text = input()
pieces = text.split()
temperatures = []
below_zero = 0

for piece in pieces:
    temperature = int(piece)
    temperatures.append(temperature)
    if temperature < 0:
        below_zero = below_zero + 1

print(f"Temperatures: {temperatures}")
print(f"Below zero: {below_zero}")
