def main():
    height = 0

    # Promp the user for input until between 1 and 8 inclusive
    while True:
        height = int(input("Please enter the height: "))

        if height >= 1 and height <= 8:
            break

    # Print two pyramides with the requested height
    for i in range(1, height + 1):
        # Get the number of whitespaces and hashes to be printed
        whitespaces = height - i
        hashes = i

        left_side = whitespaces * " " + hashes * "#"
        right_side = hashes * "#"

        print(f"{left_side}  {right_side}")

main()