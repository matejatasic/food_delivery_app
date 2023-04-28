#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = 0;

    // get the height that is
    // bigger than or equal to 1
    do
    {
        height = get_int("Choose height: ");
    }
    while (height < 1);

    for (int i = 0; i < height; i++)
    {
        // build the left side of the blocks
        for (int j = 1; j <= height; j++)
        {
            if (j >= height - i)
            {
                // printf("%i\n", j);
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }

        // print the spaces between two sides
        printf("  ");

        // build the right side of the blocks
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }

        // print new line after the rows
        // is finished
        printf("\n");
    }
}