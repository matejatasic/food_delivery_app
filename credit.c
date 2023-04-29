#include <cs50.h>
#include <stdio.h>

long SIXTEEN_DIGIT_NUMBER = 1000000000000000;
long FIFTEEN_DIGIT_NUMBER = 100000000000000;
long THIRTEEN_DIGIT_NUMBER = 1000000000000;

string VISA = "VISA";
string AMEX = "AMEX";
string MASTERCARD = "MASTERCARD";
string INVALID = "INVALID";

long getDivider(long number);

bool determineIsStartingDigitForMultiplication(long divider);

string determineCardType(long number);

int main(void)
{
    long number = 0;

    number = get_long("Type your credit card number: ");

    string cardType = determineCardType(number);

    if (cardType == INVALID)
    {
        printf("%s\n", cardType);

        return 0;
    }

    long divider = getDivider(number);
    int digit = 0;
    bool isDigitForMultiplication = determineIsStartingDigitForMultiplication(divider);
    int checksum = 0;

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
    
    bool isLastDigitZero = checksum % 10 == 0;

    if (isLastDigitZero)
    {
        printf("%s\n", cardType);

        return 0;
    }

    printf("%s\n", INVALID);
}

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