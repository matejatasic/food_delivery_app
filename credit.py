import re

VISA_REGEX = "^4\d{12,15}$"
AMEX_REGEX = "^(34|37)\d{13}$"
MASTERCARD_REGEX = "^(51|52|53|54|55)\d{14}$"

def main():
    card_number: str = str(input("Number: "))

    card_type: str = determine_card_type(card_number)

    if card_type == "INVALID":
        print(card_type)

        return

    checksum: int = calculate_checksum(card_number)

    is_last_digit_zero: bool = checksum % 10 == 0

    if is_last_digit_zero:
        print(card_type)

        return

    print("INVALID")

def determine_card_type(card_number: str) -> str:
    card_type: str = "INVALID"

    if re.search(VISA_REGEX, card_number):
        card_type = "VISA"
    elif re.search(AMEX_REGEX, card_number):
        card_type = "AMEX"
    elif re.search(MASTERCARD_REGEX, card_number):
        card_type = "MASTERCARD"

    return card_type

def calculate_checksum(card_number: str) -> int:
    checksum: int = 0
    should_multiply: bool = False

    for i in range(len(card_number) - 1, 0, -1):
        if should_multiply:
            checksum += 2 * int(i)
        else:
            checksum += int(i)

        should_multiply = !should_multiply

    return checksum

main()