#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int startingPopulation = 0;
    int endingPopulation = 0;
    int increase = 0;
    int decrease = 0;
    int numberOfYears = 0;

    // get starting population input
    while (startingPopulation < 9)
    {
        startingPopulation = get_int("Please type in the starting population size: ");
    }

    // get ending population input
    while (endingPopulation < startingPopulation)
    {
        endingPopulation = get_int("Please type in the ending population size: ");
    }

    // implement the formulas for chaning population
    // until the population is bigger than or equal
    // to the ending population size
    while (startingPopulation < endingPopulation)
    {
        increase = startingPopulation / 3;
        decrease = startingPopulation / 4;

        startingPopulation += increase;
        startingPopulation -= decrease;

        numberOfYears++;
    }

    printf("Years: %i\n", numberOfYears);
}
