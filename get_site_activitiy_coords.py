import matplotlib
matplotlib.use('Qt5Agg')  # Or 'Qt5Agg', depending on your system
import cv2 as cv
import matplotlib.pyplot as plt

def display_image(img, title=None):
    """
    Function to display an image using matplotlib. Title is specifiable as an optional argument.
    """
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    if title:
        plt.title(title)
    plt.show()

# Load the image from file
image = cv.imread('../yolov10/testimages/main_2.5x/img1.jpeg')

if image is None:
    print("Error: Could not load image. Check the file path.")
else:
    display_image(image, "Test Image")
