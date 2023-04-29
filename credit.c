#include <cs50.h>
#include <stdio.h>

long SIXTEEN_DIGIT_NUMBER = 1000000000000000;
long FIFTEEN_DIGIT_NUMBER = 100000000000000;
long THIRTEEN_DIGIT_NUMBER = 1000000000000;

string VISA = "VISA";
string AMEX = "AMEX";
string MASTERCARD = "MASTERCARD";
string INVALID = "INVALID";

bool determineIsStartingDigitForMultiplication(long divider);

string determineCardType(long number);

int calculateChecksum(long number);

long getDivider(long number);

int main(void)
{
    long number = 0;

    number = get_long("Type your credit card number: ");

    // get card type according to number length
    // and starting digits
    string cardType = determineCardType(number);

    if (cardType == INVALID)
    {
        printf("%s\n", cardType);

        return 0;
    }

    int checksum = calculateChecksum(number);
    bool isLastDigitZero = checksum % 10 == 0;

    // print the adequate card type
    // if the last digit is zero
    // otherwise print invalid
    if (isLastDigitZero)
    {
        printf("%s\n", cardType);

        return 0;
    }

    printf("%s\n", INVALID);
}

// determine if first digit is the one that will be multiplied
bool determineIsStartingDigitForMultiplication(long divider)
{
    if (divider < FIFTEEN_DIGIT_NUMBER)
    {
        return false;
    }

    else if (divider < SIXTEEN_DIGIT_NUMBER)
    {
        return false;
    }

    else
    {
        return true;
    }
}

int getStartingDigits(long number);

// determine card type based on the
// length of the number and its starting digits
string determineCardType(long number)
{
    string cardType = INVALID;
    int startingDigits = getStartingDigits(number);

    if (number < THIRTEEN_DIGIT_NUMBER)
    {

    }
    else if (number < FIFTEEN_DIGIT_NUMBER)
    {
        if (startingDigits == 4)
        {
            cardType = VISA;
        }
    }

    else if (number < SIXTEEN_DIGIT_NUMBER)
    {
        if (startingDigits == 34 || startingDigits == 37)
        {
            cardType = AMEX;
        }
    }

    else
    {
        if (
            startingDigits == 51
            || startingDigits == 52
            || startingDigits == 53
            || startingDigits == 54
            || startingDigits == 55
        )
        {
            cardType = MASTERCARD;
        }
        else if (startingDigits / 10 == 4)
        {
            cardType = VISA;
        }
    }

    return cardType;
}

// get the starting digits of a number
// based on its length
int getStartingDigits(long number)
{
    if (number < FIFTEEN_DIGIT_NUMBER)
    {
        return number / THIRTEEN_DIGIT_NUMBER;
    }

    else if (number < SIXTEEN_DIGIT_NUMBER)
    {
        return number / (FIFTEEN_DIGIT_NUMBER / 10);
    }

    else
    {
        return number / (SIXTEEN_DIGIT_NUMBER / 10);
    }
}

int calculateChecksum(long number)
{
    // get the largest divider according
    // the length of the number
    long divider = getDivider(number);
    int digit = 0;
    // check if the first digit will be
    // the one that will be multiplied and
    // accordingly multiply every other digit
    // base on the first multiplied digit
    bool isDigitForMultiplication = determineIsStartingDigitForMultiplication(divider);
    int checksum = 0;

    // get each digit and either multiply it
    // and add its digits to the checksum
    // or simpy add the digit to the checksum
    while (divider >= 1)
    {
        digit = (number / divider) % 10;

        if (isDigitForMultiplication)
        {
            digit = digit * 2;

            if (digit >= 10)
            {
                int firstDigit = digit / 10;
                int secondDigit = digit % 10;

                digit = firstDigit + secondDigit;
            }

            checksum += digit;
        }
        else
        {
            checksum += digit;
        }

        isDigitForMultiplication = !isDigitForMultiplication;

        divider /= 10;
    }

    return checksum;
}

// determine the divider based on the
// length of the number
long getDivider(long number)
{
    long result = 0;

    if (number < FIFTEEN_DIGIT_NUMBER)
    {
        return THIRTEEN_DIGIT_NUMBER;
    }

    else if (number < SIXTEEN_DIGIT_NUMBER)
    {
        return FIFTEEN_DIGIT_NUMBER;
    }

    else
    {
        return SIXTEEN_DIGIT_NUMBER;
    }
}