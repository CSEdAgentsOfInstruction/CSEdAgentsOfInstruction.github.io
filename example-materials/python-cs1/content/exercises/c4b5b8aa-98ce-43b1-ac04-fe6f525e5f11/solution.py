def read_bounded_integer(prompt, minimum, maximum):
    while True:
        text = input(prompt)

        try:
            number = int(text)
        except ValueError:
            print("Please enter an integer.")
            continue

        if number < minimum or number > maximum:
            print(f"Please enter a value from {minimum} to {maximum}.")
            continue

        return number


def main():
    level = read_bounded_integer("", 1, 5)
    print(f"Level: {level}")


main()
