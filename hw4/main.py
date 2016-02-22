__author__ = 'yihan'
from PIL import Image
import numpy
import pylab
import random
import math

def equalize_hist(input_img):
    original_width = input_img.width
    original_height = input_img.height
    output_img = Image.new("RGB", (original_width, original_height))

    resource = list(input_img.getdata())

    numOfRed = [0 for i in range(256)]
    numOfGreen = [0 for i in range(256)]
    numOfBlue = [0 for i in range(256)]
    for i in range(original_height):
       for j in range(original_width):
            numOfRed[resource[i * original_width + j][0]] += 1
            numOfGreen[resource[i * original_width + j][1]] += 1
            numOfBlue[resource[i * original_width + j][2]] += 1
    Equalize_mapping_Red = [0 for i in range(256)]
    Equalize_mapping_Green = [0 for i in range(256)]
    Equalize_mapping_Blue = [0 for i in range(256)]
    sumOfRed = 0
    sumOfGreen = 0
    sumOfBlue = 0
    for i in range(256):
        sumOfRed += numOfRed[i]
        sumOfGreen += numOfGreen[i]
        sumOfBlue += numOfBlue[i]
        Equalize_mapping_Red[i] = int(sumOfRed * 255 / (original_height * original_width))
        Equalize_mapping_Green[i] = int(sumOfGreen * 255 / (original_height * original_width))
        Equalize_mapping_Blue[i] = int(sumOfBlue * 255 / (original_height * original_width))
    result = list()
    for i in range(original_height):
       for j in range(original_width):
            tmp = []
            tmp.append(Equalize_mapping_Red[resource[i * original_width + j][0]])
            tmp.append(Equalize_mapping_Green[resource[i * original_width + j][1]])
            tmp.append(Equalize_mapping_Blue[resource[i * original_width + j][2]])
            result.append(tuple(tmp))
    output_img.putdata(result)

    return output_img

def equalize_hist_2(input_img):
    original_width = input_img.width
    original_height = input_img.height
    output_img = Image.new("RGB", (original_width, original_height))

    resource = list(input_img.getdata())

    numOfPixel = [0 for i in range(256)]
    for i in range(original_height):
       for j in range(original_width):
            numOfPixel[resource[i * original_width + j][0]] += 1
            numOfPixel[resource[i * original_width + j][1]] += 1
            numOfPixel[resource[i * original_width + j][2]] += 1
    for i in range(256):
        numOfPixel[i] /= 3
    Equalize_mapping = [0 for i in range(256)]
    sumOfPixel = 0
    for i in range(256):
        sumOfPixel += numOfPixel[i]
        Equalize_mapping[i] = int(sumOfPixel * 255 / (original_height * original_width))
    result = list()
    for i in range(original_height):
       for j in range(original_width):
            tmp = []
            tmp.append(Equalize_mapping[resource[i * original_width + j][0]])
            tmp.append(Equalize_mapping[resource[i * original_width + j][1]])
            tmp.append(Equalize_mapping[resource[i * original_width + j][2]])
            result.append(tuple(tmp))
    output_img.putdata(result)

    return output_img

def arithmetic_mean(input_img, length):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = length
    filter_height = length
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))
    weight_sum = length * length

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            sum = 0
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            sum += resource[k * original_width + l]
            if weight_sum:
                sum /= weight_sum
            result[i * original_width + j] = int(sum)

    output_img.putdata(tuple(result))
    return output_img

def geometric_mean(input_img, length):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = length
    filter_height = length
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))
    weight_sum = length * length

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            sum = 1
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            sum *= resource[k * original_width + l]
            if sum:
                sum = pow(sum, 1 / weight_sum)
            result[i * original_width + j] = int(sum)

    output_img.putdata(tuple(result))
    return output_img

def median_filter(input_img, length):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = length
    filter_height = length
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            tmp = []
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            tmp.append(resource[k * original_width + l])
            tmp.sort()
            tmp2 = 0
            if len(tmp) % 2:
                tmp2 = tmp[int((len(tmp) - 1) / 2)]
            else:
                tmp2 = (tmp[int((len(tmp) - 1) / 2)] + tmp[int(len(tmp) / 2)]) / 2
            result[i * original_width + j] = int(tmp2)

    output_img.putdata(tuple(result))
    return output_img

def max_filter(input_img, length):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = length
    filter_height = length
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            tmp = []
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            tmp.append(resource[k * original_width + l])
            tmp.sort()
            tmp2 = tmp[(len(tmp) - 1)]
            result[i * original_width + j] = int(tmp2)

    output_img.putdata(tuple(result))
    return output_img

def min_filter(input_img, length):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = length
    filter_height = length
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            tmp = []
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            tmp.append(resource[k * original_width + l])
            tmp.sort()
            tmp2 = tmp[0]
            result[i * original_width + j] = int(tmp2)

    output_img.putdata(tuple(result))
    return output_img

def harmonic_mean(input_img, length):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = length
    filter_height = length
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))
    weight_sum = length * length

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            sum = 0
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            if resource[k * original_width + l]:
                                sum += (1 / resource[k * original_width + l])
            if weight_sum and sum:
                sum = weight_sum / sum
            result[i * original_width + j] = int(sum)

    output_img.putdata(tuple(result))
    return output_img

def contraharmonic_mean(input_img, length, q):
    original_width = input_img.width
    original_height = input_img.height
    filter_width = length
    filter_height = length
    diff_width = int(filter_width / 2)
    diff_height = int(filter_height / 2)
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    for i in range(original_height):
        for j in range(original_width):
            sum = 0
            sum2 = 0
            for k in range(i - diff_height, i + diff_height + 1):
                if k >= 0 and k < original_height:
                    for l in range(j - diff_width, j + diff_width + 1):
                        if l >= 0 and l < original_width:
                            if resource[k * original_width + l]:
                                sum += pow(resource[k * original_width + l], q + 1)
                                sum2 += pow(resource[k * original_width + l], q)
            if sum2:
                sum = sum / sum2
            result[i * original_width + j] = int(sum)

    output_img.putdata(tuple(result))
    return output_img

def add_noise(input_img, noiseType, para):
    original_width = input_img.width
    original_height = input_img.height
    output_img = Image.new("L", (original_width, original_height))

    resource = list(input_img.getdata())
    result = [0 for i in range(original_width * original_height)]

    if noiseType:
        for i in range(original_height):
            for j in range(original_width):
                v1 = random.random()
                v2 = random.random()
                tmp = math.sqrt(-2 * math.log(v1)) * math.cos(2 * math.pi * v2) * para[1] + para[0];
                tmp += resource[i * original_width + j]
                result[i * original_width + j] = int(tmp)
    else:
        for i in range(original_height):
            for j in range(original_width):
                v1 = random.random()
                tmp = 0
                if v1 <= para[0]:
                    tmp = -500
                elif v1 >= 1 - para[1]:
                    tmp = 500
                tmp += resource[i * original_width + j]
                result[i * original_width + j] = int(tmp)

    output_img.putdata(tuple(result))
    return output_img

if __name__ == '__main__':
    im = Image.open("task_1.png")
    output = arithmetic_mean(im, 3)
    output.show()
    output.save("mean_1_3_3.png")

    output = arithmetic_mean(im, 9)
    output.show()
    output.save("mean_1_9_9.png")

    im = Image.open("task_1.png")
    output = harmonic_mean(im, 3)
    output.show()
    output.save("harmonic_1_3_3.png")

    output = harmonic_mean(im, 9)
    output.show()
    output.save("harmonic_1_9_9.png")

    im = Image.open("task_1.png")

    output = contraharmonic_mean(im, 3, -1.5)
    output.show()
    output.save("contraharmonic_1_3_3.png")

    output = contraharmonic_mean(im, 9, -1.5)
    output.show()
    output.save("contraharmonic_1_9_9.png")

    im = Image.open("task_2.png")

    output = add_noise(im, 1, [0, 40])
    output.show()
    output.save("Gaussian_noise.png")

    im = Image.open("Gaussian_noise.png")

    output = arithmetic_mean(im, 3)
    output.show()
    output.save("arithmetric_mean_3_3.png")

    output = geometric_mean(im, 3)
    output.show()
    output.save("geometric_mean_3_3.png")

    output = median_filter(im, 3)
    output.show()
    output.save("median_filter_3_3.png")

    im = Image.open("task_2.png")

    output = add_noise(im, 0, [0, 0.2])
    output.show()
    output.save("salt_noise.png")

    im = Image.open("salt_noise.png")

    output = harmonic_mean(im, 3)
    output.show()
    output.save("harmonic_mean_2_3_3.png")

    output = contraharmonic_mean(im, 3, 1)
    output.show()
    output.save("contraharmonic_mean_2_3_3.png")

    output = contraharmonic_mean(im, 3, -1)
    output.show()
    output.save("contraharmonic_mean_3_3_3.png")

    im = Image.open("task_2.png")

    output = add_noise(im, 0, [0.2, 0.2])
    output.show()
    output.save("salt_pepper_noise.png")

    im = Image.open("salt_pepper_noise.png")

    output = arithmetic_mean(im, 3)
    output.show()
    output.save("arithmetric_mean_2_3_3.png")

    output = geometric_mean(im, 3)
    output.show()
    output.save("geometric_mean_2_3_3.png")

    output = max_filter(im, 3)
    output.show()
    output.save("max_filter_2_3_3.png")

    output = min_filter(im, 3)
    output.show()
    output.save("min_filter_2_3_3.png")

    output = median_filter(im, 3)
    output.show()
    output.save("median_filter_2_3_3.png")

    im = Image.open("58.png")

    output = equalize_hist(im)
    output.show()
    output.save("equalize_hist.png")

    output = equalize_hist_2(im)
    output.show()
    output.save("equalize_hist_2.png")