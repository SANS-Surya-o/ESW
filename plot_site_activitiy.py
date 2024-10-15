import os
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_data_from_folder(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                data.append({
                    "filename": filename,
                    "down_foundation_people": json_data["down_foundation_work"].get("person", 0),
                    "down_foundation_trucks": json_data["down_foundation_work"].get("truck", 0),
                    "upper_structure_people": json_data["upper_structure"].get("person", 0),
                    "upper_structure_trucks": json_data["upper_structure"].get("truck", 0)
                })
    return data

def save_continuous_3d_histogram_plot(data, output_folder):
    # Extract information
    num_images = len(data)
    down_people = [d['down_foundation_people'] for d in data]
    down_trucks = [d['down_foundation_trucks'] for d in data]
    upper_people = [d['upper_structure_people'] for d in data]
    upper_trucks = [d['upper_structure_trucks'] for d in data]

    # Prepare the figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Set the positions for the bars
    x = np.arange(num_images)
    width = 0.15  # Width of the bars
    z = np.zeros(num_images)  # Z-position for the base

    # Create continuous bars for down_foundation_work
    ax.bar3d(x, z, down_people, width, 1, down_people, label='Down Foundation - People', color='skyblue', alpha=0.7)
    ax.bar3d(x, z, down_trucks, width, 1, down_trucks, label='Down Foundation - Trucks', color='lightcoral', alpha=0.7)

    # Create continuous bars for upper_structure
    ax.bar3d(x, z + 1, upper_people, width, 1, upper_people, label='Upper Structure - People', color='orange', alpha=0.7)
    ax.bar3d(x, z + 1, upper_trucks, width, 1, upper_trucks, label='Upper Structure - Trucks', color='purple', alpha=0.7)

    # Set labels
    ax.set_xlabel('Images (1 to n)')
    ax.set_ylabel('Stages')
    ax.set_zlabel('Count')

    # Set y ticks to represent stages
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(['Down Foundation', 'Upper Structure', 'Upper Structure'])

    # Title and legend
    ax.set_title('Continuous 3D Histogram of People and Trucks at Construction Sites')
    ax.legend()

    # Save the plot to the specified output folder
    output_path = os.path.join(output_folder, 'continuous_3d_histogram_people_trucks_plot.png')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()  # Close the plot to free memory

# Folder path where JSON files are stored
folder_path = 'site_count'  # Updated to the user's folder for JSON files
output_folder = 'plots'  # Output folder for saving plots

# Load data from the folder
data = load_data_from_folder(folder_path)

# Save the continuous 3D histogram plot
save_continuous_3d_histogram_plot(data, output_folder)
print(f"Continuous 3D histogram plot saved to {os.path.join(output_folder, 'continuous_3d_histogram_people_trucks_plot.png')}")
