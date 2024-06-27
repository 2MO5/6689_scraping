import fitz  # PyMuPDF for PDF text extraction
import pandas as pd  # For handling data and creating CSV files
import re  # For regular expressions to find specific text patterns

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)  # Open the PDF document
    text_data = []  # List to store text from each page
    for page_num in range(len(document)):  # Iterate through all pages
        page = document.load_page(page_num)  # Load each page
        text = page.get_text("text")  # Extract text from the page
        text_data.append(text)  # Append the extracted text to the list
    return text_data  # Return the list of text data

def parse_registration_info(text_data):
    registration_info = {
        "registration_date": [],
        "course_code": [],
        "fees": []
    }

    # Define regex patterns for the required information
    date_pattern = re.compile(r'Registration Date:\s*(\d{2}/\d{2}/\d{4})')
    course_pattern = re.compile(r'\b(EEI|EEX|MHZ|CVM|DMM|EEM)\S*\b')
    fees_pattern = re.compile(r'Fees:\s*Rs\.?\s*([\d,]+)')

    for page_text in text_data:
        # Find all matches for each pattern
        dates = date_pattern.findall(page_text)
        courses = course_pattern.findall(page_text)
        fees = fees_pattern.findall(page_text)

        # Ensure the lengths are the same by filling in with None if necessary
        max_length = max(len(dates), len(courses), len(fees))

        dates.extend([None] * (max_length - len(dates)))
        courses.extend([None] * (max_length - len(courses)))
        fees.extend([None] * (max_length - len(fees)))

        # Append each matched item to the respective list in the dictionary
        registration_info["registration_date"].extend(dates)
        registration_info["course_code"].extend(courses)
        registration_info["fees"].extend(fees)

    return registration_info

def save_to_csv(registration_info, output_path):
    df = pd.DataFrame(registration_info)  # Create a DataFrame from the parsed info
    df.to_csv(output_path, index=False)  # Save DataFrame to CSV
    print("Data extracted and saved successfully.")

pdf_path = r'C:\Users\Asus\Downloads\BSE_Student-Guidebook-2023-24.pdf'  # Path to the PDF
text_data = extract_text_from_pdf(pdf_path)  # Extract text from the PDF

registration_info = parse_registration_info(text_data)  # Parse registration information

output_path = 'student_registration_data.csv'
save_to_csv(registration_info, output_path)  # Save the parsed data to a CSV file
