name = input().strip()
destination = input().strip().lower()
weight_kg = float(input())
express_answer = input().strip().lower()

price_per_kg = 2.50
base_price = weight_kg * price_per_kg

# Classify the weight.
# Select the destination surcharge.
# Select the independent express surcharge and delivery type.
# Calculate the total and print the six-line summary.
