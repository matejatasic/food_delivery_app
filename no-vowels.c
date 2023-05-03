// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <string.h>

string replace(string word);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Too few arguments, please type in the word!\n");

        return 1;
    }

    string convertedWord = replace(argv[1]);

    printf("%s\n", convertedWord);

    return 0;
}

string replace(string word)
{
    string result = "";
    char character;

    for(int i = 0, length = strlen(word); i < length; i++)
    {
        character = word[i];

        switch(character)
        {
            case 'a':
                character = '6';
                break;
            case 'e':
                character = '3';
                break;
            case 'i':
                character = '1';
                break;
            case 'o':
                character = '0';
                break;
        }

        word[i] = character;
    }

    return word;
}
