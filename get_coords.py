import os
import json
from ultralytics import YOLO
import time
from datetime import datetime

# Global Variables
input_folder = "../yolov10/testimages/main_2.5x"  # Folder containing input images
coord_output_folder = "coordinates"  # Folder to save coordinates JSON
number_output_folder = "number"  # Folder to save counts JSON
model_path = "yolov10x.pt"  # Path to your YOLO model
confidence_treshold = 0.2  # Confidence threshold
accepted_classes = ['person', 'car', 'truck', 'bus', 'motorbike', 'bicycle']  # List of accepted classes



def store_json(model, result, filename):
    boxes = result.boxes

    # Get coordinates and class IDs
    coordinates = boxes.xyxy  # Bounding box coordinates
    class_ids = boxes.cls  # Class IDs
    class_names = model.names  # Class names

    # Create dictionaries to store results
    result_dict = {}
    count_dict = {}

    # Populate the dictionaries
    for i in range(len(coordinates)):
        class_name = class_names[int(class_ids[i])]
        coords = tuple(coordinates[i].tolist())
        if class_name not in accepted_classes:
            continue
        if class_name == 'truck' or class_name == 'bus':
            class_name = 'machinery'


        # Add coordinates to result_dict
        if class_name not in result_dict:
            result_dict[class_name] = []
        result_dict[class_name].append(coords)

        # Count object instances in count_dict
        count_dict[class_name] = count_dict.get(class_name, 0) + 1

    # Define output paths
    coord_file_path = os.path.join(coord_output_folder, f"{os.path.splitext(filename)[0]}.json")
    count_file_path = os.path.join(number_output_folder, f"{os.path.splitext(filename)[0]}_count.json")
 

    # Save coordinates to JSON
    with open(coord_file_path, 'w') as coord_file:
        json.dump(result_dict, coord_file, indent=4)

    # Save counts to JSON
    with open(count_file_path, 'w') as count_file:
        json.dump(count_dict, count_file, indent=4)
       # ALSO PUT TO MONGO DB

    print(f"Processed {filename} and saved results to {coord_file_path} and {count_file_path}")


# def process_images():
#     # Load the YOLO model
#     model = YOLO(model_path)

#     # Create output folders if they don't exist
#     os.makedirs(coord_output_folder, exist_ok=True)
#     os.makedirs(number_output_folder, exist_ok=True)

#     img_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
#                  if f.endswith(('.jpg', '.jpeg', '.png'))]

#     if batch_processing:
#         results = model(img_paths, conf=confidence_treshold)
#         for result, file_path in zip(results, img_paths):
#             filename = os.path.basename(file_path)
#             process_single_image(model, result, filename)
#     else:
#         for img_path in img_paths:
#             result = model(img_path, conf=confidence_treshold)[0]
#             filename = os.path.basename(img_path)
#             process_single_image(model, result, filename)

def get_coords(img_path):
    # Load the YOLO model
    model = YOLO(model_path)

    # Create output folders if they don't exist
    os.makedirs(coord_output_folder, exist_ok=True)
    os.makedirs(number_output_folder, exist_ok=True)

    result = model(img_path, conf=confidence_treshold)[0]
    store_json(model, result, os.path.basename(img_path))



    
# Run the image processing
if __name__ == "__main__":
    get_coords()

