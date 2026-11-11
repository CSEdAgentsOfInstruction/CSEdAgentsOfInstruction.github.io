temperature = int(input())
rain_answer = input().strip().lower()

if temperature < 5:
    print("Wear a coat.")
elif temperature < 18:
    print("Wear a jacket.")
else:
    print("A light layer is enough.")

if rain_answer == "yes":
    print("Take an umbrella.")
