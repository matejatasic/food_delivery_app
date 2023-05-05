#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int const LETTERS_LENGTH = 26;
char const LETTERS[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

bool isAllCharactersLetters(string key);
bool isAllLettersUnique(string key);
string substituteLetters(string text, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./subsitution key\n");

        return 1;
    }

    string key = argv[1];

    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");

        return 1;
    }

    if (!isAllCharactersLetters(key))
    {
        printf("Key must only containe alphabetic characters.\n");

        return 1;
    }

    if (!isAllLettersUnique(key))
    {
        printf("Key must not contain repeated characters.\n");

        return 1;
    }

    string text = get_string("plaintext: ");

    string encryptedText = substituteLetters(text, key);

    printf("ciphertext: %s\n", encryptedText);

    return 0;
}

bool isAllCharactersLetters(string key)
{
    for (int i = 0, length = strlen(key); i < length; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
    }

    return true;
}

bool isAllLettersUnique(string key)
{
    int lettersCount[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    char keyLetter;

    for (int i = 0, length = strlen(key); i < length; i++)
    {
        keyLetter = tolower(key[i]);

        for (int j = 0; j < LETTERS_LENGTH; j++)
        {
            if(lettersCount[j] > 1) {
                return false;
            }

            if (LETTERS[j] == keyLetter)
            {
                lettersCount[j]++;
            }
        }
    }

    return true;
}

string substituteLetters(string text, string key)
{
    char textLetter;
    char substituteLetter;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        textLetter = text[i];

        for (int j = 0; j < LETTERS_LENGTH; j++)
        {
            if (LETTERS[j] == tolower(textLetter))
            {
                substituteLetter = key[j];

                if (islower(textLetter))
                {
                    substituteLetter = tolower(key[j]);
                }

                text[i] = substituteLetter;
            }
        }
    }

    return text;
}