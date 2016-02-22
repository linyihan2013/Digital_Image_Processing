__author__ = 'yihan'
from PIL import Image

def scale(input_img, size):
    original_width = input_img.width
    original_height = input_img.height
    target_width = size[0]
    target_height = size[1]
    scale_width = original_width / target_width
    scale_height = original_height / target_height
    output_img = Image.new("L", size)

    resource = list(input_img.getdata())
    result = []
    for i in range(target_height):
       for j in range(target_width):
            result.append(resource[int(i * scale_height) * original_width + int(j * scale_width)])
    output_img.putdata(tuple(result))
    return output_img

def quantize(input_img, level):
    original_width = input_img.width
    original_height = input_img.height
    output_img = Image.new("L", (original_width, original_height))
    level_height = int(255 / (level - 1))

    resource = list(input_img.getdata())
    result = []
    for i in range(original_height):
       for j in range(original_width):
           result.append(int(resource[i * original_width + j] / level_height) * level_height)
    output_img.putdata(tuple(result))
    return output_img

if __name__ == '__main__':
    im = Image.open("58.png")
    output = scale(im, (192, 128))
    output.show("1")
    output.save("192_128.png")
    output = scale(im, (96, 64))
    output.show("2")
    output.save("96_64.png")
    output = scale(im, (48, 32))
    output.show("3")
    output.save("48_32.png")
    output = scale(im, (24, 16))
    output.show("4")
    output.save("24_16.png")
    output = scale(im, (12, 8))
    output.show("5")
    output.save("12_8.png")

    output = scale(im, (300, 200))
    output.show("6")
    output.save("300_200.png")

    output = scale(im, (450, 300))
    output.show("7")
    output.save("450_300.png")

    output = scale(im, (500, 200))
    output.show("8")
    output.save("500_200.png")

    output = quantize(im, 128)
    output.show("9")
    output.save("128grey.png")

    output = quantize(im, 32)
    output.show("10")
    output.save("32grey.png")

    output = quantize(im, 8)
    output.show("11")
    output.save("8grey.png")

    output = quantize(im, 4)
    output.show("12")
    output.save("4grey.png")

    output = quantize(im, 2)
    output.show("13")
    output.save("2grey.png")