import json
import os


read_from = "coordinates"
output_to = "site_count"


def inside(box1, box2):
    x0_1, y0_1, x1_1, y1_1 = box1  # First bounding box
    x0_2, y0_2, x1_2, y1_2 = box2  # Second bounding box

    # Check if there is an overlap
    return (x0_1 >= x0_2 and y0_1 >= y0_2 and  # Top-left corner of box1 inside box2
            x1_1 <= x1_2 and y1_1 <= y1_2)    # Bottom-right corner of box1 inside box2



def count_objects():

    with open('site_activities.json', 'r') as activity_file:
        activities = json.load(activity_file)


    output_folder = read_from
    number_folder = output_to

    # Create the number folder if it doesn't exist
    os.makedirs(number_folder, exist_ok=True)

    # Iterate through all .json files in the 'output' folder
    for filename in os.listdir(output_folder):
        if filename.endswith('.json'):  # Only process JSON files
            input_file_path = os.path.join(output_folder, filename)

        with open(input_file_path, 'r') as output_file:
            detections = json.load(output_file)

        result_dict = {}

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

        # Save the result in number/img_name.json
            output_file_path = os.path.join(number_folder, f'{os.path.splitext(filename)[0]}.json')
            with open(output_file_path, 'w') as outfile:
                json.dump(result_dict, outfile, indent=4)

            print(f'Processed {filename} and saved to {output_file_path}')

count_objects()