from PIL import Image
from reportlab.pdfgen import canvas
import io

def image_with_opacity(img: Image, opacity: float):
    if opacity < 0 or opacity > 1:
        raise ValueError("Opacity must be between 0 and 1")

    aimg = img.convert("RGBA")

    # Create an alpha mask for the opacity
    r, g, b, a = aimg.split()  # Get the alpha channel
    a = a.point(lambda p: p * opacity)  # Apply the opacity
    new_image = Image.merge("RGBA", (r, g, b, a))
    return new_image

def concat_images(img1: Image, img2: Image):
    """
    Lay two images on top of each other.

    Args:
        img1 (PIL.Image): The first image.
        img2 (PIL.Image): The second image.

    Returns:
        PIL.Image: The combined image.
    """
    imgnew = Image.new("RGBA", (max(img1.width, img2.width), max(img1.height, img2.height)))
    imgnew.paste(img1.convert("RGBA"), (0, 0))
    imgnew.paste(img2.convert("RGBA"), (0, 0))
    return imgnew

def lay_image(img1, img2):
    img2 = img2.resize((img1.width, img1.height))
    new_image = Image.new("RGBA", (max(img1.width, img2.width), max(img1.height, img2.height)))
    new_image.paste(img1, (0, 0))
    new_image.paste(img2, (0, 0), mask=img2.split()[3])
    return new_image

if __name__ == "__main__":
    img1 = Image.open("csim.jpg")
    image_with_opacity(img1, 0.3).save("temp_image.png")
    img1 = Image.open("scatterplot.png").crop((125, 95, 900, 714))
    img2 = Image.open("temp_image.png")
    lay_image(img1, img2).save("temp_image2.png")
    # im = Image.open("scatterplot.png").crop((125, 95, 900, 714))
    # im.save("temp_image2.png")