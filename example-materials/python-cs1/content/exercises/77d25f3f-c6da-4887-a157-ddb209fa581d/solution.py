count = int(input())
titles = []

for number in range(count):
    titles.append(input())

search_term = input()
matching_titles = []

search_term = search_term.lower()

for title in titles:
    if search_term in title.lower():
        matching_titles.append(title)

print(f"Matches: {matching_titles}")
