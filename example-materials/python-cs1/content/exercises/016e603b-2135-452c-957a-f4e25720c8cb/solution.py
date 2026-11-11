text = input()
items = text.split(",")

print(f"Item count: {len(items)}")

for item in items:
    print(item.strip())
