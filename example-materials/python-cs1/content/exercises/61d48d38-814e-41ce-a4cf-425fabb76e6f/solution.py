cards = []

for number in range(5):
    cards.append(int(input()))

strictly_increasing = True

for index in range(len(cards) - 1):
    if cards[index] >= cards[index + 1]:
        strictly_increasing = False

print(f"Strictly increasing: {strictly_increasing}")
