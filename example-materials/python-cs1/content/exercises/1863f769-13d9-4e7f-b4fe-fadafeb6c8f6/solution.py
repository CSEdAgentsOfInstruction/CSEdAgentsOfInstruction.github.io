count = int(input())
words = []

for number in range(count):
    words.append(input())

long_word_count = 0

for word in words:
    if len(word) >= 5:
        long_word_count = long_word_count + 1

print(f"Words with at least 5 characters: {long_word_count}")
