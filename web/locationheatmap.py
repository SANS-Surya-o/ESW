import matplotlib.pyplot as plt
import os
import json
from PIL import Image
import io

def get_json_coords_data(jsondir: str) -> list[dict]:
    """
    Loads JSON data from all files in the specified directory.

    Args:
        jsondir (str): The directory containing JSON files.

    Returns:
        list: A list of JSON objects (python dicts) loaded from files in the directory.

    Raises:
        Exception: If the specified directory does not exist.
    """
    print("Obtaining endopoint data from " + jsondir)
    data = []
    if os.path.exists(jsondir):
        for file in os.listdir(jsondir):
            if file.endswith(".json"):
                with open(f"{jsondir}/{file}") as f:
                    data.append(json.load(f))
    else:
        raise Exception("Directory does not exist")
    return data

def get_midpoint_coords(dicts: list[dict]) -> tuple[list, list]:
    """
    Get all the midpoint coordinates of all the machinery and people in the data.

    Returns:
        tuple: A tuple of two lists, where the first list contains the x coordinates of the machinery and the second list contains the x coordinates of the people.
    """
    print("Obtaining midpoint coordinates")
    machinery = [[], []]
    people = [[], []]

    for dict in dicts:
        for key, arrays in dict.items():
            if key != 'machinery' and key != 'person':
                continue
            for arr in arrays:
                if key == 'machinery':
                    machinery[0].append((arr[0]+arr[2])/2)
                    machinery[1].append((arr[1]+arr[3])/2)
                if key == 'person':
                    people[0].append((arr[0]+arr[2])/2)
                    people[1].append((arr[1]+arr[3])/2)
    return machinery, people

# [
#     {'truck': [[1478.5938720703125, 502.3048400878906, 1532.3486328125, 561.4503784179688], 
#                 [1542.346435546875, 534.2078247070312, 1600.0, 656.0631713867188]], 
#     'person': [[241.93650817871094, 622.060791015625, 259.1118469238281, 670.3052368164062], 
#                 [45.32514953613281, 816.5474243164062, 72.62866973876953, 850.076904296875], 
#                 [76.0182876586914, 776.9659423828125, 96.94563293457031, 832.6947631835938], 
#                 [1526.5062255859375, 567.1476440429688, 1544.7509765625, 616.1315307617188], 
#                 [1225.077392578125, 475.66015625, 1237.267333984375, 514.8869018554688], 
#                 [167.92218017578125, 769.3246459960938, 190.35671997070312, 841.4072265625], 
#                 [142.13589477539062, 776.1769409179688, 159.98045349121094, 805.8267822265625], 
#                 [291.6562805175781, 604.7528686523438, 305.0070495605469, 640.2249145507812], 
#                 [169.6390838623047, 769.9949951171875, 192.15322875976562, 841.4030151367188], 
#                 [170.6714630126953, 770.2278442382812, 189.5510711669922, 841.2929077148438]], 
#     'boat': [[641.6561279296875, 531.8693237304688, 711.2353515625, 579.4697875976562]]
#     }
# ]

# print(people)

def scatter_plot(machinery: list[list], people: list[list]) -> Image:
    """
    Creates a scatter plot of truck and people locations and returns it as an Image.

    Args:
        machinery (list[list]): A list of two lists containing x and y coordinates of machinery.
        people (list[list]): A list of two lists containing x and y coordinates of people.

    Returns:
        Image: A PIL Image object of the scatter plot with truck and people locations.
    """
    print("Creating scatter plot")
    # Create the scatter plot
    plt.figure(figsize=(10, 8))
    plt.scatter([-x for x in machinery[0]], machinery[1], c = 'red', marker = 'o', label='machinery')
    plt.scatter([-x for x in people[0]], people[1], c = 'green', marker = 'o', label='People')
    plt.title('Location heatmap')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    # Save the scatter plot as a PNG image in memory
    scatter_img_buffer = io.BytesIO()
    plt.savefig(scatter_img_buffer, format = 'png')
    scatter_img = Image.open(scatter_img_buffer)
    return scatter_img