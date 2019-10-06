"""
A lossy compression algorithm. Decoding tool.
"""

import numpy as np
import os
import argparse
from PIL import Image


def decode(number, file):
    """
    takes number of pictures to decompress and nparray with compressed pictures
    creates a directory with decompressed pictures
    """
    # loading an array
    array = np.load(file)

    # checking, if thr number is correct
    if number > array[0, 0, 0, 0]:
        raise Exception('Only %d pictures compressed in the array!'
                        % array[0, 0, 0, 0])
    if number <= 0:
        raise Exception('You cannot decompress less than a one picture!')

    # creating a matrix of zeros to replace its values then
    matrix = np.zeros((array.shape[0] - 1, array.shape[1],
                       array.shape[2], number), dtype=float)

    # ndarray with y-coordinates of the sample points
    ycoords = np.linspace(0, number - 1, number)

    for row in range(1, array.shape[0]):
        for col in range(array.shape[1]):
            for pix in range(array.shape[2]):
                # creating polynomial class
                poly = np.poly1d(array[row, col, pix])
                # replacing pixel's values by approximated coefficients
                matrix[row - 1, col, pix] = poly(ycoords)

    # creating a matrix of zeros to replace it with rgb image values then
    image = np.zeros((array.shape[0] - 1, array.shape[1],
                       array.shape[2]), 'uint8')

    # creating a directory
    path = 'output%d_%d' % (array.shape[3] - 1, number)
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed." % path)
    else:
        print("Successfully created the directory %s." % path)

    for img in range(number):
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                for pix in range(image.shape[2]):
                    if matrix[row, col, pix, img] < 0:
                        image[row, col, pix] = 0
                    elif matrix[row, col, pix, img] > 255:
                        image[row, col, pix] = 255
                    else:
                        image[row, col, pix] = matrix[row, col, pix, img]

        # saving an image as .png file
        image2 = Image.fromarray(image.astype('uint8'))
        image2.save('%s/new_output00%d.png' % (path, img + 10))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A algorithm that decompress \
        .png files from nparray.")
    parser.add_argument("-n", "--number",
                        help="A number of pictures to decompress.",
                        type=int, required=True)
    parser.add_argument("-a", "--nparray",
                        help="A nparray with compressed pictures.",
                        required=True)
    args = parser.parse_args()

    decode(args.number, args.nparray)
