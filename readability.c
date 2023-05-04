#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    int numberOfLetters = count_letters(text);
    int numberOfWords = count_words(text);
    int numberOfSentences = count_sentences(text);

    float lettersPer100Words = (float)numberOfLetters / numberOfWords * 100.00;
    float sentencesPer100Words = (float)numberOfSentences / numberOfWords * 100.00;

    int index = round(0.0588 * lettersPer100Words - 0.296 * sentencesPer100Words - 15.8);

    if(index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if(index < 1)
    {
        printf("Before Grade 1\n");
    }
    else {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int numberOfLetters = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalnum(text[i]))
        {
            numberOfLetters++;
        }
    }

    return numberOfLetters;
}

int count_words(string text)
{
    int numberOfWords = 1;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isblank(text[i]))
        {
            numberOfWords++;
        }
    }

    return numberOfWords;
}

int count_sentences(string text)
{
    int numberOfSentences = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (
            text[i] == '.'
            || text[i] == '!'
            || text[i] == '?'
        )
        {
            numberOfSentences++;
        }
    }

    return numberOfSentences;
}