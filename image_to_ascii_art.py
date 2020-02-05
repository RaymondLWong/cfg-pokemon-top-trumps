import io

from PIL import Image


def image_to_ascii_art(img_data, output_width=120):
    img = Image.open(io.BytesIO(img_data))

    # resize the image
    width, height = img.size
    aspect_ratio = height / width
    new_width = output_width
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    # new size of image
    # print(img.size)

    # convert image to greyscale format
    # https://stackoverflow.com/questions/52307290/what-is-the-difference-between-images-in-p-and-l-mode-in-pil
    img = img.convert('L')

    pixels = img.getdata()

    # replace each pixel with a character from array
    chars = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
    new_pixels = [chars[pixel // 25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image
