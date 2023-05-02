#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int const ALPHABET_SIZE = 26;
// Points assigned to each letter of the alphabet
int POINTS[ALPHABET_SIZE] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
// Letters of the alphabet
char LETTERS[ALPHABET_SIZE] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

int compute_score(string word);
int getCharacterScore(char character, int alphabetSize);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 == score2)
    {
        printf("Tie!\n");
    }
    else if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else
    {
        printf("Player 2 wins!\n");
    }
}

int compute_score(string word)
{
    int score = 0;
    int charPoint = 0;

    for(int i = 0, length = strlen(word); i < length; i++)
    {
        charPoint = getCharacterScore(word[i], ALPHABET_SIZE);
        score += charPoint;
    }

    return score;
}

int getCharacterScore(char character, int alphabetSize)
{
    for(int i = 0; i < alphabetSize; i++)
    {
        if (LETTERS[i] == tolower(character))
        {
            return POINTS[i];
        }
    }

    return 0;
}