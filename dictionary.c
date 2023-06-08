// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * 26;

// Hash table
node *table[N];

int words_in_dictionary = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_index = hash(word);
    node *pointer = table[hash_index];

    while(pointer != NULL)
    {
        if (strcasecmp(pointer->word, word) == 0)
        {
            return true;
        }

        node *next = pointer->next;
        pointer = next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int first_letter_index = toupper(word[0]) - 'A';
    int second_letter_index = toupper(word[1]) - 'A';

    if(second_letter_index < 0)
    {
        second_letter_index = 0;
    }

    return (first_letter_index * 26) + second_letter_index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dictionary_file = fopen(dictionary, "r");

    if(dictionary_file == NULL)
    {
        printf("Could not open %s\n", dictionary);
        return false;
    }

    char *word = malloc(LENGTH + 1);
    node *list = NULL;

    while(fscanf(dictionary_file, "%s", word) != EOF)
    {
        words_in_dictionary++;

        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        n->next = NULL;
        strcpy(n->word, word);

        int hash_index = hash(word);

        if(table[hash_index] == NULL)
        {
            table[hash_index] = n;
        }
        else {
            n->next = table[hash_index];

            table[hash_index] = n;
        }

        n->next = list;
        list = n;
    }

    free(word);

    fclose(dictionary_file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return words_in_dictionary;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *row = table[i];

        while (row != NULL)
        {
            if(isalnum(row->word[0]))
            {
                printf("%s\n", row->word);
            }
            node *tmp = row;
            row = tmp->next;
            free(row);
        }
    }

    return true;
}
