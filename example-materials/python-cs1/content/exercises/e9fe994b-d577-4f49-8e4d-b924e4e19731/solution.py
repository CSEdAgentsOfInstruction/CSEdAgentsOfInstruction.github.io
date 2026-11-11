scores = []

while True:
    text = input().strip().lower()

    if text == "stop":
        break

    scores.append(int(text))

print(scores)
