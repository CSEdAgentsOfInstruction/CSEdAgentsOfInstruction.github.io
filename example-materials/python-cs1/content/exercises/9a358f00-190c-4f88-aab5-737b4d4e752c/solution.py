# Workshop reference solution.
word = input().strip().lower()

vowel_count = 0
for character in word:
    if character in "aeiou":
        vowel_count = vowel_count + 1

print(vowel_count)
