import json
import os


coordinates_folder = "coordinates"
number_folder = "site_count"


def inside(box1, box2):
    x0_1, y0_1, x1_1, y1_1 = box1  # First bounding box
    x0_2, y0_2, x1_2, y1_2 = box2  # Second bounding box

    # Check if there is an overlap
    return (x0_1 >= x0_2 and y0_1 >= y0_2 and  # Top-left corner of box1 inside box2
            x1_1 <= x1_2 and y1_1 <= y1_2)    # Bottom-right corner of box1 inside box2



def count_objects(filename):
    # Construct the full input file path from coordinates_folder
    input_file_path = os.path.join(coordinates_folder, filename)

    # Validate if the input file exists and is a JSON file
    if not filename.endswith('.json'):
        print("Invalid filename passed. Please provide a JSON file.")
        return

    if not os.path.exists(input_file_path):
        print(f"File {filename} not found in {coordinates_folder}")
        return

    # Load the activities from the 'site_activities.json' file
    with open('site_activities.json', 'r') as activity_file:
        activities = json.load(activity_file)

    # Create the number_folder if it doesn't exist
    os.makedirs(number_folder, exist_ok=True)

    # Load the detections from the input file
    with open(input_file_path, 'r') as output_file:
        detections = json.load(output_file)

    # Dictionary to store results
    result_dict = {}

    # Iterate through activities and their bounding boxes
    for activity, activity_box in activities.items():
        result_dict[activity] = {}  # Initialize the nested dictionary for this activity

        # Iterate through detected objects in the current image
        for object_name, object_boxes in detections.items():
            count = 0
            # Check each detected object's bounding box
            for object_box in object_boxes:
                # If the bounding box is inside the activity bounding box
                if inside(object_box, activity_box):
                    count += 1  # Count the object

            # Only store if there was at least one object found inside the activity
            result_dict[activity][object_name] = count

    # Construct the output file path in the number_folder
    output_file_path = os.path.join(number_folder, filename)

    # Save the results to the output file
    with open(output_file_path, 'w') as outfile:
        json.dump(result_dict, outfile, indent=4)

    print(f'Processed {filename} and saved to {output_file_path}')




if __name__ == "__main__":
    count_objects()
