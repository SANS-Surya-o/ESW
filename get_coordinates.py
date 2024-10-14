import os
import json
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2
# from analysis import count_objects





def process_single_image(model,result,filename,output_folder):
        boxes = result.boxes
        


        # Do the BOUNDING BOXES WORK LATER
        # result.save(save_dir=output_folder)  # This saves the images with bounding boxes

        # Get coordinates and class IDs
        coordinates = boxes.xyxy  # Bounding box coordinates
        class_ids = boxes.cls      # Class IDs
        class_names = model.names   # Class names

        # Create a dictionary to store results
        result_dict = {}

        # Populate the dictionary
        for i in range(len(coordinates)):
            class_name = class_names[int(class_ids[i])]
            coords = tuple(coordinates[i].tolist())

            # Initialize a list for this class if it doesn't exist
            if class_name not in result_dict:
                result_dict[class_name] = []

            # Append the coordinates to the list for this class
            result_dict[class_name].append(coords)

        # Define output file path
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.json")

        # Write the result_dict to the output file in a human-readable format
        with open(output_file_path, 'w') as outfile:
            json.dump(result_dict, outfile, indent=4)

        # Print the result image with bounding boxes
        print(f"Processed {filename} and saved results to {output_file_path}")

        # # Display the image with bounding boxes
        # result_image_path = os.path.join(output_folder, os.path.basename(results_path))
        # img = cv2.imread(result_image_path)
        # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for display in matplotlib
        # plt.imshow(img_rgb)
        # plt.axis('off')
        # plt.show()





















def process_images(input_folder, output_folder, model_path, confidence_threshold=0.5,batch_processing=False):
    # Load the YOLO model
    model = YOLO(model_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    img_paths = []
    for filename in os.listdir(input_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):  # Check for image files
                image_path = os.path.join(input_folder, filename)
                img_paths.append(image_path)

    if batch_processing:
    # Iterate through each image in the input folder
        # Run inference on the image with the specified confidence threshold
        results = model(img_paths, conf=confidence_threshold)

        # Save the output image with bounding boxes to the output folder
        # ~~~~~~~~~~~~~~results_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_bbox.jpg")

        # Access the first result
        for result, file_paths in zip(results, img_paths):
            filename = os.path.basename(file_paths)
            process_single_image(model,result,filename,output_folder)

    else:
        for img_path in img_paths:
            # Run inference on the image with the specified confidence threshold
            result = model(img_path, conf=confidence_threshold)
            filename = os.path.basename(img_path)
            # print(os.path.basename(img_path))

            # Save the output image with bounding boxes to the output folder
            # results_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(img_path))[0]}_bbox.jpg")

            # Access the first result
            process_single_image(model,result[0],filename,output_folder)

        
                
       

# Specify paths
input_folder = "input_images"  # Folder containing input images
output_folder = "output"        # Folder to save output files
model_path = "yolov10x.pt"       # Path to your YOLO model
confidence_treshold = 0.2
batch_processing = False
# Call the function to process images
process_images(input_folder, output_folder, model_path,confidence_treshold,batch_processing)
# count_objects()
