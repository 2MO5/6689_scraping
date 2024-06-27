import fitz  # PyMuPDF for PDF text extraction
import pandas as pd  # For handling data and creating CSV files
import re  # For regular expressions to find specific text patterns

def extract_text_from_pdf(pdf_path):
    guide_book = fitz.open(pdf_path)  # Open the PDF document
    text_data = []  # List to store text from each page
    for page_number in range(len(guide_book)):  # Iterate through all pages
        page = guide_book.load_page(page_number)  # Load each page
        pdf_text = page.get_text("text")  # Extract text from the page
        text_data.append(pdf_text)  # Append the extracted text to the list
    return text_data  # Return the list of text data

#function to parse registration info
def parse_registration_info(text_data):
    registration_info = {
        "registration_date": [],
        "required_courses": [],
        "fees": [],
        "payment_details": []
    }

    # Define regex patterns for the required information
    date_pattern = re.compile(r'Registration Date:\s*(\d{2}/\d{2}/\d{4})')
    course_pattern = re.compile(r'\b(EEI|EEX|MHZ|CVM|DMM|EEM)\S*\b')
    fees_pattern = re.compile(r'Fees:\s*Rs\.?\s*([\d,]+)')
    payment_pattern = re.compile(r'Payment Details:\s*(.*)')

    for page_text in text_data:
        # Find registration dates
        dates = date_pattern.findall(page_text)
        registration_info["registration_date"].extend(dates)

        # Find required courses
        courses = course_pattern.findall(page_text)
        registration_info["required_courses"].extend(courses)

        # Find fees
        fees = fees_pattern.findall(page_text)
        registration_info["fees"].extend(fees)

        # Find payment details
        payments = payment_pattern.findall(page_text)
        registration_info["payment_details"].extend(payments)

    # Ensure all lists in the dictionary are of the same length
    max_length = max(len(registration_info[key]) for key in registration_info)
    for key in registration_info:
        while len(registration_info[key]) < max_length:
            registration_info[key].append(None)  # Append None to lists that are shorter

    return registration_info


#function to save as csv
def save_to_csv(registration_info, output_path):
    df = pd.DataFrame(registration_info)  # Create a DataFrame from the parsed info
    df.to_csv(output_path, index=False)  # Save DataFrame to CSV
    print("Data extracted and saved successfully.")

pdf_path = r'C:\Users\Asus\Downloads\BSE_Student-Guidebook-2023-24.pdf'  # Path to the PDF
text_data = extract_text_from_pdf(pdf_path)  # Extract text from the PDF

registration_info = parse_registration_info(text_data)  # Parse registration information

output_path = 'student_registration_data.csv'
save_to_csv(registration_info, output_path)  # Save the parsed data to a CSV file
