// #include <getopt.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

const int WAV_HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("Usage ./reverse arg1 arg2\n");

        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *inputFile = fopen(argv[1], "r");

    if (inputFile == NULL)
    {
        printf("Could not open %s\n", argv[1]);
    }

    // Read header
    // TODO #3
    WAVHEADER wavHeader;

    fread(&wavHeader, sizeof(WAVHEADER), 1, inputFile);

    // Use check_format to ensure WAV format
    // TODO #4
    if (!check_format(wavHeader))
    {
        printf("%s is not a valid .wav file", argv[1]);
    }

    // Open output file for writing
    // TODO #5
    FILE *outputFile = fopen(argv[2], "w");

    if (outputFile == NULL)
    {
        fclose(inputFile);
        printf("Could not create %s", argv[2]);
    }

    // Write header to file
    // TODO #6
    fwrite(&wavHeader, sizeof(WAVHEADER), 1, outputFile);

    // Use get_block_size to calculate size of block
    // TODO #7

    int blockSize = get_block_size(wavHeader);

    // Write reversed audio to file
    // TODO #8
    uint8_t  audioBlock[blockSize];
    long d;

    fseek(inputFile, blockSize, SEEK_END);

    while (ftell(inputFile) - blockSize > WAV_HEADER_SIZE)
    {
        fseek(inputFile, -2 * blockSize, SEEK_CUR);
        fread(&audioBlock, blockSize, 1, inputFile);
        fwrite(&audioBlock, blockSize, 1, outputFile);
    }

    fclose(outputFile);
    fclose(inputFile);
}

int check_format(WAVHEADER header)
{
    // TODO #4
    // char *format = header.format;
    if (
        header.format[0] == 'W'
        && header.format[1] == 'A'
        && header.format[2] == 'V'
        && header.format[3] == 'E'
    )
    {
        return 1;
    }

    return 0;
}

int get_block_size(WAVHEADER header)
{
    return header.numChannels * (header.bitsPerSample / 8);
}