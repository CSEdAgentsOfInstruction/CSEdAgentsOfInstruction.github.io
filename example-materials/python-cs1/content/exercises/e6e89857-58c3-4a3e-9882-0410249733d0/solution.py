session_pages = []

while True:
    text = input().strip().lower()

    if text == "done":
        break

    session_pages.append(int(text))

total_pages = 0

for pages in session_pages:
    total_pages = total_pages + pages

print(f"Sessions: {len(session_pages)}")
print(f"Total pages: {total_pages}")
