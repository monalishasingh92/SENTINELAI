import pymupdf
from PIL import Image, ImageDraw

# Create an image containing safety instructions
image = Image.new("RGB", (1200, 500), "white")
draw = ImageDraw.Draw(image)

draw.text((50, 50), "WORKPLACE SAFETY RULES", fill="black")
draw.text((50, 150), "1. Workers must wear safety helmets.", fill="black")
draw.text((50, 220), "2. Safety goggles are required.", fill="black")
draw.text((50, 290), "3. Keep emergency exits clear.", fill="black")
draw.text((50, 360), "4. Report hazards immediately.", fill="black")

# Save image temporarily
image_path = "backend/rag/test_documents/scanned_page.png"
image.save(image_path)

# Create a PDF containing only the image
pdf = pymupdf.open()
page = pdf.new_page(width=600, height=250)

page.insert_image(
    page.rect,
    filename=image_path
)

pdf_path = "backend/rag/test_documents/scanned_test.pdf"
pdf.save(pdf_path)
pdf.close()

print("Scanned PDF created successfully:", pdf_path)