#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = "";

    // get the name
    name = get_string("Hello, what is your name? ");

    printf("hello, %s\n", name);
}