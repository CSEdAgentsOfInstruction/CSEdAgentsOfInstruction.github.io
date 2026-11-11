reference_text = input()
typed_text = input()

reference_words = reference_text.lower().split()
typed_words = typed_text.lower().split()

correct_positions = 0

for index in range(len(reference_words)):
    if reference_words[index] == typed_words[index]:
        correct_positions = correct_positions + 1

print(f"Correct positions: {correct_positions} of {len(reference_words)}")
