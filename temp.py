from pdf2image import convert_from_path

# Path to the PDF file you want to convert
pdf_file_path = "transcript_1.pdf"

# Convert the PDF to a list of PIL Image objects
images = convert_from_path(pdf_file_path)

# Specify the output directory and format (PNG)
output_dir = 'output_images/'
image_format = 'PNG'

# Save each page as a PNG image
for i, image in enumerate(images):
    image.save(f'{output_dir}page_{i + 1}.{image_format.lower()}', image_format)

print(f'PDF pages converted to {image_format} format and saved in {output_dir}')
