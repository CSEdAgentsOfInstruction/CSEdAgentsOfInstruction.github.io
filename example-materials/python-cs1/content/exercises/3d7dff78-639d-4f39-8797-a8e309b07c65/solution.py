# Workshop reference solution.
word = input().strip().lower()

count = 0
for character in word:
    if character == "a":
        count = count + 1

print(count)
