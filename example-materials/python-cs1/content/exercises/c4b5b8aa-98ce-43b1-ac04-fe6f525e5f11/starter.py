def read_bounded_integer(prompt, minimum, maximum):
    text = input(prompt)
    return int(text)


def main():
    level = read_bounded_integer("", 1, 5)
    print(f"Level: {level}")


main()
