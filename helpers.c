#include "helpers.h"
#include <stdio.h>

// This function changes the color of the black pixels
void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE pixel;

    // Iterate over the pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            pixel = image[i][j];

            // If the pixel is black, change it to light blue
            if (
                pixel.rgbtRed == 0
                && pixel.rgbtGreen == 0
                && pixel.rgbtBlue == 0
            )
            {
                image[i][j].rgbtRed = 102;
                image[i][j].rgbtGreen = 204;
                image[i][j].rgbtBlue = 255;
            }
        }
    }
}
