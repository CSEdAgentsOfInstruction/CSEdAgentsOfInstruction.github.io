name = input().strip()
destination = input().strip().lower()
weight_kg = float(input())
express_answer = input().strip().lower()

price_per_kg = 2.50
base_price = weight_kg * price_per_kg

if weight_kg < 2:
    weight_class = "light"
elif weight_kg <= 10:
    weight_class = "standard"
else:
    weight_class = "heavy"

if destination == "local":
    destination_surcharge = 0
elif destination == "national":
    destination_surcharge = 4
else:
    destination_surcharge = 12

express_surcharge = 0
delivery_type = "standard"

if express_answer == "yes":
    express_surcharge = 6
    delivery_type = "express"

total_price = base_price + destination_surcharge + express_surcharge

print(f"Name: {name}")
print(f"Destination: {destination}")
print(f"Weight class: {weight_class}")
print(f"Base price: {base_price:.2f} euros")
print(f"Delivery: {delivery_type}")
print(f"Total price: {total_price:.2f} euros")
