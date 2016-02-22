__author__ = 'yihan'
from PIL import Image
import numpy
import pylab

def equalize_hist(input_img):
    original_width = input_img.width
    original_height = input_img.height
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    bins = numpy.arange(0, 256, 1)
    pylab.hist(resource, bins)
    pylab.xlabel('Before Equalization')
    pylab.show()

    numOfGray = [0 for i in range(256)]
    for i in range(original_height):
       for j in range(original_width):
           numOfGray[resource[i * original_width + j]] += 1
    Equalize_mapping = [0 for i in range(256)]
    sum = 0
    for i in range(256):
        sum += numOfGray[i]
        Equalize_mapping[i] = int(sum * 255 / (original_height * original_width))
    result = []
    for i in range(original_height):
       for j in range(original_width):
           result.append(Equalize_mapping[resource[i * original_width + j]])
    output_img.putdata(tuple(result))

    bins = numpy.arange(0, 256, 1)
    pylab.hist(result, bins)
    pylab.xlabel('After Equalization')
    pylab.show()

    return output_img

def filter2d(input_img, filter):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = len(filter[0])
    filter_height = len(filter)
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))
    weight_sum = 0
    for i in range(filter_height):
        for j in range(filter_width):
            weight_sum += filter[i][j]

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            sum = 0
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            sum += resource[k * original_width + l] * filter[k - i + diff_height][l - j + diff_width]
            if weight_sum:
                sum /= weight_sum
            result[i * original_width + j] = int(sum)

    output_img.putdata(tuple(result))
    return output_img

if __name__ == '__main__':
    im = Image.open("58.png")
    original_data = list(im.getdata())
    output = equalize_hist(im)
    output.show()
    output.save("After_Equalization.png")

    output = filter2d(im, [[1 for i in range(3)] for j in range(3)])
    output.show()
    output.save("3_3_AveragingFilter.png")

    output = filter2d(im, [[1 for i in range(7)] for j in range(7)])
    output.show()
    output.save("7_7_AveragingFilter.png")

    output = filter2d(im, [[1 for i in range(11)] for j in range(11)])
    output.show()
    output.save("11_11_AveragingFilter.png")

    laplacian = filter2d(im, [[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    laplacian_data = list(laplacian.getdata())
    for i in range(im.height):
        for j in range(im.width):
            laplacian_data[i * im.width + j] = original_data[i * im.width + j] - laplacian_data[i * im.width + j]
    laplacian.putdata(tuple(laplacian_data))
    laplacian.show()
    laplacian.save("LaplacianFilter.png")

    averaging_filter = filter2d(im, [[1 for i in range(3)] for j in range(3)])
    filter_data = list(averaging_filter.getdata())
    boost_data = [0 for i in range(im.width * im.height)]
    for i in range(im.height):
        for j in range(im.width):
            boost_data[i * im.width + j] = 3 * (original_data[i * im.width + j] - filter_data[i * im.width + j]) + original_data[i * im.width + j]
    high_boost = Image.new("L", (im.width, im.height))
    high_boost.putdata(tuple(boost_data))
    high_boost.show()
    high_boost.save("high_boost.png")