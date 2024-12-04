from flask import Flask, jsonify, request, render_template
from PIL import Image
from datetime import datetime
import os
from get_coords import get_coords
from cnt_nums import count_objects
from reportlab.pdfgen import canvas
from io import BytesIO
app = Flask(__name__)

image_output_folder = "images"
OUTPUT_PDF_PATH = "./output/generated_images.pdf"
PLOTS_FOLDER = "./plots"
NUMBER_FOLDER = "./number"
SITE_CNT_FOLDER = "./site_count"

if not os.path.exists(image_output_folder):
    os.makedirs(image_output_folder)


@app.route('/image', methods=['POST'])
def check():
    # Get the uploaded image from the request
    image_file = request.files.get('image')
    if image_file:
        # Convert the image to a PIL Image for further processing
        image = Image.open(image_file)
        
        # Generate a timestamp-based filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = f"{timestamp}.jpg"  # You can adjust the file format (e.g., PNG)
        
        # Save the image to the specified folder
        image_path = os.path.join(image_output_folder, image_filename)
        image.save(image_path)
        get_coords(image_path)
        count_objects(f"{timestamp}.json")
        

        # Perform your image analysis here (e.g., call a function for object detection)
        
        # Return the success response
        return jsonify({"status": "success", "message": "Image received and processed", "image_path": image_path}), 200
    else:
        return jsonify({"status": "error", "message": "No image received"}), 400


@app.route('/get_jsons', methods=['GET'])
def get_jsons():
    # Get the number of JSONs the client wants
    count = int(request.args.get('count', 1))

    # List of all JSON files to be returned
    json_data = []

    # Function to get the latest JSON files from a folder
    def get_latest_jsons(folder, count):
        files = [f for f in os.listdir(folder) if f.endswith('.json')]
        files.sort(reverse=True)  # Sort by filename in descending order (latest first)
        latest_files = files[:count]  # Get the latest `count` files
        
        # Read the JSON data from the selected files
        data = []
        for filename in latest_files:
            with open(os.path.join(folder, filename), 'r') as f:
                json_content = json.load(f)
            timestamp = int(filename.split('.')[0])  # Extract timestamp from filename
            data.append({"timestamp": timestamp, "data": json_content})
        
        return data

    # Get the latest JSONs from both folders
    json_data.extend(get_latest_jsons(NUMBER_FOLDER, count))
    json_data.extend(get_latest_jsons(SITE_CNT_FOLDER, count))

    # Sort all the JSON data by timestamp in descending order (latest first)
    json_data.sort(key=lambda x: x['timestamp'], reverse=True)

    # Return the JSON data to the client
    return jsonify(json_data[:count])



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)