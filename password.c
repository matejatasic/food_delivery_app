// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    bool hasOneUppercase = false;
    bool hasOneLowercase = false;
    bool hasOneNumber = false;
    bool hasOneSpecialChar = false;

    for (int i = 0, length = strlen(password); i < length; i++)
    {
        if (isupper(password[i]))
        {
            hasOneUppercase = true;
        }
        else if (islower(password[i]))
        {
            hasOneLowercase = true;
        }
        else if (isdigit(password[i]))
        {
            hasOneNumber = true;
        }
        else {
            hasOneSpecialChar = true;
        }
    }

    if (
        hasOneUppercase
        && hasOneLowercase
        && hasOneNumber
        && hasOneSpecialChar
    )
    {
        return true;
    }

    return false;
}
