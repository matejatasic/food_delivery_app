#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = "";

    name = get_string("Hello, what is your name? ");

    printf("hello, %s\n", name);
}