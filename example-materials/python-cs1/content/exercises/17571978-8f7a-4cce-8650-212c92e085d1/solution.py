people = int(input())
slices_per_person = int(input())
slices_per_pizza = 8

total_slices = people * slices_per_person
pizzas = (total_slices + slices_per_pizza - 1) // slices_per_pizza
print(f"Pizzas: {pizzas}")
