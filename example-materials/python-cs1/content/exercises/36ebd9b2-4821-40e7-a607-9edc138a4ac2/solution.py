# Workshop reference solution.
count = int(input())
words = []

for number in range(count):
    words.append(input())

long_words = []

for index in range(len(words)):
    if len(words[index]) >= 5:
        long_words.append(words[index])

print(f"Original: {words}")
print(f"Long words: {long_words}")
