import fitz  # PyMuPDF
from PIL import Image
import pytesseract


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]

        # Get the images on the page
        images = page.get_images(full=True)

        for img_index, img_info in enumerate(images):
            # Get the image
            base_image = pdf_document.extract_image(img_info)
            image_bytes = base_image["image"]

            # Convert the image bytes to a PIL Image
            image = Image.open(io.BytesIO(image_bytes))

            # Use Tesseract OCR to extract text
            text = pytesseract.image_to_string(image)

            print(f"Page {page_number + 1}, Image {img_index + 1}:\n{text}\n")

    # Close the PDF file
    pdf_document.close()


# Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_path = 'your_pdf_file.pdf'

# Call the function to extract text from the PDF
extract_text_from_pdf(pdf_path)
