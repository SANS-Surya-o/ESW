import os

# this code will reaname all the images in the format imgi.jpg

def rename_images(folder_path):
    # Get a list of all files in the folder
    images = os.listdir(folder_path)

    # Rename each image
    for i, image in enumerate(images, start=1):
        old_path = os.path.join(folder_path, image)
        new_name = f"img{i}{os.path.splitext(image)[1]}"  # Retain original file extension
        new_path = os.path.join(folder_path, new_name)
        
        # Rename the image
        os.rename(old_path, new_path)
        print(f"Renamed {image} to {new_name}")

# Specify the folder path containing images
folder_path = "../yolov10/testimages/main_2.5x"                   # folder in which u want to rename
rename_images(folder_path)