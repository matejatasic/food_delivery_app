import re

VISA_REGEX = "^4\d{12,15}$"
AMEX_REGEX = "^(34|37)\d{13}$"
MASTERCARD_REGEX = "^(51|52|53|54|55)\d{14}$"


def main():
    # Getthe input from the user as a string
    card_number: str = str(input("Number: "))

    # Determine the type of card
    card_type: str = determine_card_type(card_number)

    if card_type == "INVALID":
        print(card_type)

        return

    # Calculate the checksum using the Luhn's Algorithm
    checksum: int = calculate_checksum(card_number)

    # Check if last digit is a zero
    is_last_digit_zero: bool = checksum % 10 == 0

    # Print the card type
    if is_last_digit_zero:
        print(card_type)

        return

    print("INVALID")


# Determine the card type based on card regexes
def determine_card_type(card_number: str) -> str:
    card_type: str = "INVALID"

    if re.search(VISA_REGEX, card_number):
        card_type = "VISA"
    elif re.search(AMEX_REGEX, card_number):
        card_type = "AMEX"
    elif re.search(MASTERCARD_REGEX, card_number):
        card_type = "MASTERCARD"

    return card_type


# Calculate checksum by using the Luhn's Algorithm
def calculate_checksum(card_number: str) -> int:
    checksum: int = 0
    should_multiply: bool = False

    # Iterate over the card number backwards and add them to
    # the checksum or add the digits that resulted from multiplicating
    # the digit by 2
    for i in range(len(card_number) - 1, -1, -1):
        if should_multiply:
            number = 2 * int(card_number[i])

            if number >= 10:
                first_digit = number // 10
                second_digit = number % 10
                number = first_digit + second_digit

            checksum += number
        else:
            checksum += int(card_number[i])

        should_multiply = not should_multiply

    return checksum


main()
