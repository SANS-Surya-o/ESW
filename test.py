from flask import Flask, jsonify, request
from PIL import Image
from datetime import datetime
import os
from get_coords import get_coords
from cnt_nums import count_objects
app = Flask(__name__)

image_output_folder = "images"

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



    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)