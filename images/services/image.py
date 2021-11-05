import imagehash

from io import BytesIO
from PIL import Image


def get_image_hashing(image):
    return imagehash.phash(Image.open(image))


def get_image_dimensions(image):
    return Image.open(image).size


def scale_image(image, scale=1):
    new_image = Image.open(image)

    # Высчитываем новые размеры изображения
    new_width = round(new_image.width * scale)
    new_height = round(new_image.height * scale)

    new_image = new_image.resize((new_width, new_height), Image.ANTIALIAS)

    # Сохраняем измененное изображение в памяти
    output = BytesIO()
    new_image.save(fp=output, format='JPEG')

    # Получаем измененное изображение из памяти
    return output.getvalue()
