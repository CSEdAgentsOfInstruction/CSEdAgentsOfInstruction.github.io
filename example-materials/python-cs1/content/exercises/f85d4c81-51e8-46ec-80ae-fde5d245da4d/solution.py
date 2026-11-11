word = input().strip().lower()

for character in word:
    if character in "aeiou":
        print(character)
