from reportlab.platypus import Paragraph, SimpleDocTemplate, Image as RLImage, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
import locationheatmap as lh
import images
from PIL import Image

def make_pdf():
    parastyle = ParagraphStyle(
        name='BodyText',
        fontSize=12,
        leading=15,
        spaceAfter=25,
        fontName='Helvetica'
    )

    titlestyle = ParagraphStyle(
        name='Title',
        fontSize=20,
        leading=40,
        fontName='Helvetica-Bold'
    )

    t1 = Paragraph("Activity report", titlestyle)
    para = Paragraph("Given below is a heatmap of the coordinates of the trucks and people. It provides a good visual understanding of where most of the work is going on.", parastyle)

    trucks, people = lh.get_midpoint_coords(lh.get_json_coords_data("coordinates"))
    sp = lh.scatter_plot(trucks, people)
    sp.save("scatterplot.png", format = "png")
    images.lay_image(sp.crop((125, 95, 900, 714)), images.image_with_opacity(Image.open("csim.jpg"), 0.5)).save("temp_image.png", format = 'png')
    img = RLImage('x.png', width = 6*inch, height = 4.5*inch)

    para2 = Paragraph("Here are some more plots on when objects (people or machinery) are entering and leaving the site. This will provide some more insights.", parastyle)

    img2 = RLImage('plots/continuous_3d_histogram_people_trucks_plot.png', width = 6.5*inch, height = 4.5*inch)

    img3 = RLImage('plots/object_counts_over_time.png', width = 6*inch, height = 4*inch)

    doc = SimpleDocTemplate("report.pdf")
    doc.build([t1, para, img, PageBreak(), para2, img2, img3])

if __name__ == "__main__":
    make_pdf()