#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

void copyImage(int height, int width, RGBTRIPLE copy[height][width], RGBTRIPLE originalImage[height][width]);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average;
    RGBTRIPLE pixel;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // divide by 3.0 to get the float and round it to the nearest integer
            pixel = image[i][j];
            average = round((pixel.rgbtBlue + pixel.rgbtGreen + pixel.rgbtRed) / 3.0);

            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }

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

            // use the formula for each color to get the sepia effect
            red = round(.393 * pixel.rgbtRed + .769 * pixel.rgbtGreen + .189 * pixel.rgbtBlue);
            green = round(.349 * pixel.rgbtRed + .686 * pixel.rgbtGreen + .168 * pixel.rgbtBlue);
            blue = round(.272 * pixel.rgbtRed + .534 * pixel.rgbtGreen + .131 * pixel.rgbtBlue);

            // if the value of any color is bigger than 255, set it to 255
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
        k = width - 1;

        // reverse each row to get the reflection effect
        for (int j = 0; j < width / 2; j++)
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
    float pixelsCounted;
    int red;
    int green;
    int blue;
    int currentRowInd;
    int currentColumnInd;

    copyImage(height, width, copy, image);

    for (int rowInd = 0; rowInd < height; rowInd++)
    {
        for (int columnInd = 0; columnInd < width; columnInd++)
        {
            red = 0;
            green = 0;
            blue = 0;
            pixelsCounted = 0.00;
            for (int i = -1; i < 2; i++)
            {
                for (int j = -1; j < 2; j++)
                {
                    currentRowInd = rowInd + i;
                    currentColumnInd = columnInd + j;

                    if (
                        currentRowInd < 0
                        || currentRowInd > (height - 1)
                        || currentColumnInd < 0
                        || currentColumnInd > (width - 1)
                    )
                    {
                        continue;
                    }

                    red += image[currentRowInd][currentColumnInd].rgbtRed;
                    green += image[currentRowInd][currentColumnInd].rgbtGreen;
                    blue += image[currentRowInd][currentColumnInd].rgbtBlue;

                    pixelsCounted++;
                }

                copy[rowInd][columnInd].rgbtRed = round(red / pixelsCounted);
                copy[rowInd][columnInd].rgbtGreen = round(green / pixelsCounted);
                copy[rowInd][columnInd].rgbtBlue = round(blue / pixelsCounted);
            }
        }
    }

    for(int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }

    return;
}

void copyImage(int height, int width, RGBTRIPLE copy[height][width], RGBTRIPLE originalImage[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = originalImage[i][j];
        }
    }
}
