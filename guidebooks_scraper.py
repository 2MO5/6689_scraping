import fitz  # PyMuPDF
import pandas as pd

#function to extract text
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)  # Open the PDF document
    text_data = []  # List to store text from each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)  # Load each page
        text = page.get_text("text")  # Extract text from the page
        text_data.append(text)  # Append the extracted text to the list
    return text_data

#defining pdf path and extracting data to text
pdf_path = r'C:\Users\Asus\Downloads\BSE_Student-Guidebook-2023-24.pdf'  # path to the guidebook and creating a raw string
text_data = extract_text_from_pdf(pdf_path)  # Extract text from the PDF

# Save the extracted text to a CSV file
df = pd.DataFrame(text_data, columns=['Text'])
df.to_csv('bse_student_guidebook_data1.csv', index=False)
print("Data extracted and saved successfully.")
