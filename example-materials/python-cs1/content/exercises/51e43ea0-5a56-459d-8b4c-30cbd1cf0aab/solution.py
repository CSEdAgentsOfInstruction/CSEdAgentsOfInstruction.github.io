count = int(input())
words = []

for number in range(count):
    words.append(input())

total_characters = 0

for word in words:
    total_characters = total_characters + len(word)

print(f"Total characters: {total_characters}")
