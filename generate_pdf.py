from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from io import BytesIO
from PIL import Image

# Path to the folder containing images
PLOTS_FOLDER = "./plots"
OUTPUT_PDF_PATH = "./output/generated_images.pdf"


def generate_pdf():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PDF_PATH), exist_ok=True)

    # Create a new PDF
    pdf = canvas.Canvas(OUTPUT_PDF_PATH, pagesize=letter)
    page_width, page_height = letter

    # Get all image file paths in the plots folder
    image_files = [os.path.join(PLOTS_FOLDER, f) for f in os.listdir(PLOTS_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        return "No images found in the plots folder.", 404

    y_position = page_height - 50  # Start from the top of the page
    margin = 50  # Left margin for images
    image_height_limit = page_height - 100  # Maximum height for images

    for image_path in image_files:
        # Open the image to get its dimensions
        img = Image.open(image_path)
        img_width, img_height = img.size

        # Scale the image to fit within the PDF page, preserving aspect ratio
        scale = min((page_width - 2 * margin) / img_width, image_height_limit / img_height)
        new_width = img_width * scale
        new_height = img_height * scale

        # If the image doesn't fit on the current page, create a new one
        if y_position - new_height < 50:
            pdf.showPage()  # Start a new page
            y_position = page_height - 50  # Reset y position to top

        # Draw the image on the PDF
        pdf.drawImage(image_path, margin, y_position - new_height, width=new_width, height=new_height)

        # Update the y position for the next image
        y_position -= (new_height + 20)  # Leave space for the next image

    pdf.save()  # Save the PDF to the file

if __name__ == "__main__":
    generate_pdf()