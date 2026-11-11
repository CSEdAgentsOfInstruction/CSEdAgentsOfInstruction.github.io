word = input().strip().lower()
highlighted = ""

for character in word:
    if character in "aeiou":
        highlighted = highlighted + character.upper()
    else:
        highlighted = highlighted + character

print(highlighted)
