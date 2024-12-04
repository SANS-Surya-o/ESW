import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
from PIL import Image
import os
import json
from reportlab.lib.pagesizes import letter

def add_image_with_opacity(c : canvas.Canvas, image_filename, x, y, width, height, opacity):
    # Create a temporary image with reduced opacity
    original_image = Image.open(image_filename).convert("RGBA")
    
    # Create an alpha mask for the opacity
    alpha = original_image.split()[3]  # Get the alpha channel
    alpha = alpha.point(lambda p: p * opacity)  # Apply the opacity
    new_image = Image.new("RGBA", original_image.size)
    new_image.paste(original_image, (0, 0), alpha)
    
    # Save the new image temporarily
    temp_image_filename = "temp_image.png"
    new_image.save(temp_image_filename)

    # Create a PDF and add the image
    c.drawImage(temp_image_filename, x, y, width, height)
    # c.save()


def make_white_less_opaque_in_image(imgbuf: io.BytesIO):
    img = Image.open(imgbuf)
    datas = img.convert("RGBA").getdata()
    newData = []
    for item in datas:
        # print(item)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 100))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(imgbuf)
    imgbuf.seek(0)
    # img.save(path)

def get_json_data():
    data = []
    if os.path.exists("../output2"):
        for file in os.listdir("../output2"):
            if file.endswith(".json"):
                with open(f"../output2/{file}") as f:
                    data.append(json.load(f))
    return data

dicts = get_json_data()

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

trucks = [[], []]
people = [[], []]

for dict in dicts:
    for key, arrays in dict.items():
        if key != 'truck' and key != 'person':
            continue
        for arr in arrays:
            if key == 'truck':
                trucks[0].append((arr[0]+arr[2])/2)
                trucks[1].append((arr[1]+arr[3])/2)
            if key == 'person':
                people[0].append((arr[0]+arr[2])/2)
                people[1].append((arr[1]+arr[3])/2)

# print(people)

def generateReport(trucks : list, people: list):

    # Create the scatter plot
    plt.figure(figsize=(10, 8))
    plt.scatter(trucks[0], trucks[1], c = 'red', marker = 'o', label='Trucks')
    plt.scatter(people[0], people[1], c = 'green', marker = 'o', label='People')
    plt.title('Location heatmap')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()

    # Save the scatter plot as a PNG image in memory
    scatter_img_buffer = io.BytesIO()
    plt.savefig(scatter_img_buffer, format = 'png')
    scatter_img = Image.open(scatter_img_buffer)
    make_white_less_opaque_in_image(scatter_img)
    scatter_img.save('scatterplot.png', format = 'png')
    scatter_img_buffer.seek(0)

    # Create a PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    c.setFillColorRGB(0, 0, 0)
    c.rect(0, 0, c._pagesize[0], c._pagesize[1], fill = 1)
    c.setFillColorRGB(1, 1, 1)

    # Add a title to the PDF
    c.setFont("Helvetica", 16)
    c.drawString(50, 750, "Activity Report")
    add_image_with_opacity(c, "csim.jpg", 50, 0, 500, 400, 0.5)
    c.drawImage(ImageReader(scatter_img_buffer), 50, 0, width = 500, height = 400)


    c.showPage()

    # Add some text below the heatmap
    c.setFont("Helvetica", 10)
    c.drawString(50, 350, "This heatmap shows a randomly generated 10x10 matrix.")
    c.drawString(50, 330, "The colors represent the values in the matrix, with darker colors")
    c.drawString(50, 310, "indicating lower values and brighter colors indicating higher values.")

    c.save()

    # Save the PDF to a file
    with open("heatmap_report.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())

    print("PDF report 'heatmap_report.pdf' has been generated.")

if __name__ == "__main__":
    generateReport(trucks, people)
