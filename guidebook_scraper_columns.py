import fitz  # PyMuPDF
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text_data = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")
        text_data.append(text)
    return text_data

def parse_registration_info(text_data):
    registration_info = {
        "registration_date": [],
        "course_code": [],
        "fees": []
    }

    date_pattern = re.compile(r'Registration Date:\s*(\d{2}/\d{2}/\d{4})')
    course_pattern = re.compile(r'\b(EEI|EEX|MHZ|CVM|DMM|EEM)\d{4}\b')
    fees_pattern = re.compile(r'Rs\.?\s*([\d,]+) per credit')

    fee_per_credit = 0

    for page_text in text_data:
        dates = date_pattern.findall(page_text)

        courses_with_credits = course_pattern.findall(page_text)
        course_codes = [course for course in courses_with_credits if course[1] in '3456']
        credits = [int(course[1]) for course in courses_with_credits if course[1] in '3456']

        fees_match = fees_pattern.search(page_text)
        if fees_match:
            fee_per_credit = int(fees_match.group(1).replace(',', ''))

        total_fees = [credit * fee_per_credit for credit in credits]

        max_length = max(len(dates), len(course_codes), len(total_fees))

        dates.extend([None] * (max_length - len(dates)))
        course_codes.extend([None] * (max_length - len(course_codes)))
        total_fees.extend([None] * (max_length - len(total_fees)))

        registration_info["registration_date"].extend(dates)
        registration_info["course_code"].extend(course_codes)
        registration_info["fees"].extend(total_fees)

    return registration_info

def save_to_csv(registration_info, output_path):
    df = pd.DataFrame(registration_info)
    df.to_csv(output_path, index=False)
    print("Data extracted and saved successfully.")

# Path to the PDF
pdf_path = r'C:\Users\Asus\Downloads\BSE_Student-Guidebook-2023-24.pdf'
text_data = extract_text_from_pdf(pdf_path)

registration_info = parse_registration_info(text_data)

output_path = 'student_registration_data.csv'
save_to_csv(registration_info, output_path)
