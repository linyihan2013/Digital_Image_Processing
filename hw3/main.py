__author__ = 'yihan'
from PIL import Image
import numpy
import pylab
from math import e, pi

def dft2d(input_img, flags):
    original_width = input_img.width
    original_height = input_img.height
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    if flags == 1:                                                      #DFT
        for i in range(original_height):
             for j in range(original_width):
                 resource[i * original_width + j] *= pow(-1, i + j)
        fxv = [0 for i in range(original_width * original_height)]
        for i in range(original_height):
           for j in range(original_width):
               for m in range(original_height):
                   fxv[i * original_width + j] += resource[m * original_width + j] * \
                            pow(e, complex(0, -2 * pi * (i * m / original_height)))
        for i in range(original_height):
           for j in range(original_width):
                for n in range(original_width):
                   result[i * original_width + j] += fxv[i * original_width + n] * \
                        pow(e, complex(0, -2 * pi * (j * n / original_width)))
                result[i * original_width + j] /= original_width
                result[i * original_width + j] = result[i * original_width + j].real
                print(i * original_width + j)
    else:                                                                #IDFT
        fxv = [0 for i in range(original_width * original_height)]
        for i in range(original_height):
           for j in range(original_width):
               for m in range(original_height):
                   fxv[i * original_width + j] += resource[m * original_width + j] * \
                            pow(e, complex(0, 2 * pi * (i * m / original_height)))
        for i in range(original_height):
           for j in range(original_width):
                for n in range(original_width):
                   result[i * original_width + j] += fxv[i * original_width + n] * \
                        pow(e, complex(0, 2 * pi * (j * n / original_width)))
                result[i * original_width + j] = result[i * original_width + j].real
                result[i * original_width + j] *= pow(-1, i + j)
                print(i * original_width + j)

    output_img.putdata(tuple(result))
    return output_img

def filter2d_freq(input_img, filter):
    original_width = input_img.width
    original_height = input_img.height
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            resource[i * original_width + j] *= pow(-1, i + j)
    fxv = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            for m in range(original_height):
                fxv[i * original_width + j] += resource[m * original_width + j] * \
                    pow(e, complex(0, -2 * pi * (i * m / original_height)))

    for i in range(original_height):
        for j in range(original_width):
            for n in range(original_width):
               result[i * original_width + j] += fxv[i * original_width + n] * \
                    pow(e, complex(0, -2 * pi * (j * n / original_width)))
            result[i * original_width + j] /= original_width

#

    filter_width = len(filter[0])
    filter_height = len(filter)
    filter_input = [0 for i in range(original_width * original_height)]
    filter_data = [0 for i in range(original_width * original_height)]
    fxv = [0 for i in range(original_width * original_height)]
    sum_weight = 0
    for i in range(filter_height):
        for j in range(filter_width):
            sum_weight += filter[i][j]
            filter[i][j] *= pow(-1, i + j)
            filter_input[i * original_width + j] = filter[i][j]
    for i in range(original_height):
        for j in range(original_width):
            for m in range(original_height):
                fxv[i * original_width + j] += filter_input[m * original_width + j] * \
                    pow(e, complex(0, -2 * pi * (i * m / original_height)))

    for i in range(original_height):
        for j in range(original_width):
            for n in range(original_width):
                filter_data[i * original_width + j] += fxv[i * original_width + n] * \
                    pow(e, complex(0, -2 * pi * (j * n / original_width)))
            filter_data[i * original_width + j] /= original_width
            result[i * original_width + j] *= filter_data[i * original_width + j]
            print(result[i * original_width + j])
#

    fxv = [0 for i in range(original_width * original_height)]
    for i in range(original_height):
        for j in range(original_width):
            for m in range(original_height):
                fxv[i * original_width + j] += result[m * original_width + j] * \
                    pow(e, complex(0, 2 * pi * (i * m / original_height)))
    result = [0 for i in range(original_width * original_height)]
    for i in range(original_height):
        for j in range(original_width):
            for n in range(original_width):
                result[i * original_width + j] += fxv[i * original_width + n] * \
                        pow(e, complex(0, 2 * pi * (j * n / original_width)))
            result[i * original_width + j] /= original_width
            result[i * original_width + j] = result[i * original_width + j].real
            result[i * original_width + j] *= pow(-1, i + j)
            result[i * original_width + j] *= 20
            print(result[i * original_width + j])

    if sum_weight == 0:                                                                  #Laplacian
        for i in range(original_height):
            for j in range(original_width):
                resource[i * original_width + j] *= pow(-1, i + j)
                result[i * original_width + j] = resource[i * original_width + j] - 10 * result[i * original_width + j]

    output_img.putdata(tuple(result))
    return output_img

if __name__ == '__main__':
    im = Image.open("58.png")
    output = dft2d(im, 1)
    output.show()
    output.save("DFT.png")

    im = Image.open("DFT.png")
    output = dft2d(im, 2)
    output.show()
    output.save("IDFT.png")

    im = Image.open("58.png")
    output = filter2d_freq(im, [[1 for j in range(7)] for i in range(7)])
    output.show()
    output.save("7_7_Averaging.png")

    im = Image.open("58.png")
    output = filter2d_freq(im, [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    output.show()
    output.save("LaplacianFilter.png")