import os
import json
import matplotlib.pyplot as plt

# Global variables
number_output_folder = "number"  # Folder containing count JSON files
plots_folder = "plots"  # Folder to save plots

def load_counts_from_files():
    """Loads object counts from the JSON files in chronological order."""
    counts_over_time = []  # List to store counts from each time step
    filenames = sorted(os.listdir(number_output_folder))  # Ensure chronological order

    # Iterate through sorted files to maintain time order
    for filename in filenames:
        if filename.endswith('.json'):
            file_path = os.path.join(number_output_folder, filename)
            with open(file_path, 'r') as f:
                counts = json.load(f)
            counts_over_time.append(counts)

    return counts_over_time

def aggregate_data(counts_over_time):
    """Aggregates counts for all object classes across all time steps."""
    # Extract all unique object class names from the data
    all_classes = set()
    for counts in counts_over_time:
        all_classes.update(counts.keys())

    # Initialize an empty dictionary to store time series data for each class
    aggregated_data = {cls: [] for cls in all_classes}

    # Populate the time series data with object counts (fill with 0 if not present)
    for counts in counts_over_time:
        for cls in aggregated_data:
            aggregated_data[cls].append(counts.get(cls, 0))

    return aggregated_data

def save_plot(aggregated_data, output_path):
    """Saves the counts of each object class over time as an image."""
    plt.figure(figsize=(10, 6))

    # Plot the time series for each object class
    for cls, counts in aggregated_data.items():
        plt.plot(counts, label=cls, marker='o')

    plt.xlabel("Time (Chronological Order)")
    plt.ylabel("Number of Objects")
    plt.title("Object Counts Over Time")
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to the specified output path
    plt.savefig(output_path)
    plt.close()  # Close the plot to free up memory

def main():
    # Load counts from files and aggregate them
    counts_over_time = load_counts_from_files()
    aggregated_data = aggregate_data(counts_over_time)

    # Create the plots folder if it doesn't exist
    os.makedirs(plots_folder, exist_ok=True)

    # Define the output file path for the plot image
    output_path = os.path.join(plots_folder, "object_counts_over_time.png")

    # Save the plot to the specified path
    save_plot(aggregated_data, output_path)
    print(f"Plot saved to {output_path}")

# Run the main function
if __name__ == "__main__":
    main()
