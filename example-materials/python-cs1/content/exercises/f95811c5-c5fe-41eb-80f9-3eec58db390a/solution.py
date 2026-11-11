# Workshop reference solution.
count = int(input())
scores = []

for number in range(count):
    scores.append(int(input()))

for index in range(len(scores)):
    scores[index] = scores[index] + 1

print(scores)
