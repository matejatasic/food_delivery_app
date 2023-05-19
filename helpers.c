#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void copyImage(int height, int width, RGBTRIPLE copy[height][width], RGBTRIPLE oritiginalImage[height][width]);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average;
    RGBTRIPLE pixel;

    for (int i = 0; i < height; i++) // iterate through rows
    {
        for (int j = 0; j < width; j++) // iterate through pixels
        {
            RGBTRIPLE pixel = image[i][j];
            // divide by 3.0 and then round in order to get a float that will round up if ending >= .5 (default for dividing integers by integers is rounding down)
            int average = round((pixel.rgbtBlue + pixel.rgbtGreen + pixel.rgbtRed) / 3.0);

            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    // for (int i = 0; i < height; i++)
    // {
    //     for (int j = 0; j < width; j++)
    //     {
    //         pixel = image[i][j];
    //         average = (pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) / 3.00;
    //         image[i][j].rgbtRed = round(average);
    //         image[i][j].rgbtGreen = round(average);
    //         image[i][j].rgbtBlue = round(average);
    //     }
    // }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE pixel;
    long red;
    long green;
    long blue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            pixel = image[i][j];
            red = round(.393 * pixel.rgbtRed + .769 * pixel.rgbtGreen + .189 * pixel.rgbtBlue);
            green = round(.349 * pixel.rgbtRed + .686 * pixel.rgbtGreen + .168 * pixel.rgbtBlue);
            blue = round(.272 * pixel.rgbtRed + .534 * pixel.rgbtGreen + .131 * pixel.rgbtBlue);

            if (red > 255)
            {
                red = 255;
            }

            if (green > 255)
            {
                green = 255;
            }

            if (blue > 255)
            {
                blue = 255;
            }

            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    int k;

    for (int i = 0; i < height; i++)
    {
        k = width;

        for (int j = 0, length = width / 2; j < length; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][k];
            image[i][k] = temp;
            k--;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    RGBTRIPLE pixel;

    copyImage(height, width, copy, image);

    for (int i = 0; i < height; i++)
    {
        for (int l = 0; l < width; l++)
        {
            int redSum = copy[i][l].rgbtRed;
            int greenSum = copy[i][l].rgbtGreen;
            int blueSum = copy[i][l].rgbtBlue;
            int pixelsCounted = 0;

            if (l > 0)
            {
                redSum += copy[i][l-1].rgbtRed;
                greenSum += copy[i][l-1].rgbtGreen;
                blueSum += copy[i][l-1].rgbtBlue;
                pixelsCounted++;
            }

            if(l < width)
            {
                redSum += copy[i][l+1].rgbtRed;
                greenSum += copy[i][l+1].rgbtGreen;
                blueSum += copy[i][l+1].rgbtBlue;
                pixelsCounted++;
            }

            if (i != 0)
            {
                for (int j = 0; j < width; j++)
                {
                    if(abs(l - j) > 1)
                    {
                        break;
                    }

                    redSum += copy[i-1][j].rgbtRed;
                    greenSum += copy[i-1][j].rgbtGreen;
                    blueSum += copy[i-1][j].rgbtBlue;
                    pixelsCounted++;
                }
            }

            if (i != height) {
                for (int k = 0; k < width; k++)
                {
                    if(abs(l - k) > 1)
                    {
                        break;
                    }

                    redSum += copy[i+1][k].rgbtRed;
                    greenSum += copy[i+1][k].rgbtGreen;
                    blueSum += copy[i+1][k].rgbtBlue;
                    pixelsCounted++;
                }
            }

            image[i][l].rgbtRed = redSum / pixelsCounted;
            image[i][l].rgbtGreen = greenSum / pixelsCounted;
            image[i][l].rgbtBlue = blueSum / pixelsCounted;
        }
    }

    return;
}

void copyImage(int height, int width, RGBTRIPLE copy[height][width], RGBTRIPLE oritiginalImage[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = oritiginalImage[i][j];
        }
    }
}
