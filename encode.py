"""
A lossy compression algorithm. Encoding tool.
"""

import glob
import numpy as np
import argparse
from PIL import Image


def encode(degree, path):
    """
    takes degree of polynominal, directory of .png files
    compresses and saves the pictures as .npy matrix
    """
    # creating sorted list of files
    files = sorted(glob.glob('%s/*.png' % path))

    # checking, if there were pictures
    if len(files) == 0:
        raise Exception('There are not any files in the given directory!')
    # checking, if the degree of a polynomial is correct
    if degree >= len(files) or degree < 1:
        raise Exception('Wrong degree of a polynomial.')

    # creating a matrix of images' matrices
    images = np.array([np.array(Image.open(file).convert('RGB'))
                       for file in files])

    # creating a rgb like matrix but with all pictures' values
    matrix = np.array([[[[images[l][i][j][k]
                          for l in range(images.shape[0])]
                         for k in range(images.shape[3])]
                        for j in range(images.shape[2])]
                       for i in range(images.shape[1])])

    # creating a matrix of zeros to replace its values then
    new_matrix = np.zeros((matrix.shape[0] + 1, matrix.shape[1],
                           matrix.shape[2], degree + 1), dtype=float)

    # inserting to matrix information, how many pictures have been compressed
    # new_matrix[0, 0, 0, 0] = len(files)
    new_matrix[0, 0, 0, 0] = 60

    # ndarray with y-coordinates of the sample points
    ycoords = np.linspace(0, len(matrix[0, 0, 0]) - 1, len(matrix[0, 0, 0]))

    for row in range(1, new_matrix.shape[0]):
        for col in range(new_matrix.shape[1]):
            for pix in range(new_matrix.shape[2]):
                # fitting a polynomial
                coeff = np.polyfit(ycoords, matrix[row - 1, col, pix],
                                   degree, full=True)
                # replacing pixel's values by approximated coefficients
                new_matrix[row, col, pix] = coeff[0]

    # saving an array as .npy binary file
    np.save('app_pics.npy', new_matrix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A lossy compression \
        algorithm that compress similar .png pictures to .npy matrix.")
    parser.add_argument("-d", "--degree", help="A degree of polynomial.",
                        type=int, required=True)
    parser.add_argument("-p", "--path",
                        help="A directory of pictures, you want to compress.",
                        required=True)
    args = parser.parse_args()

    encode(args.degree, args.path)
