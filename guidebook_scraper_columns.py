import tabula
import pandas as pd
import re

# Function to calculate credit value from course code
def calculate_credit(course_code):
    try:
        # The second digit of the course code represents the credit value
        credit_value = int(course_code[1])
        return credit_value
    except (IndexError, ValueError):
        # Return a default credit value or handle the error
        return 0  # or raise an error

# Function to calculate cost from credit value
def calculate_cost(credit):
    cost_per_credit = 2000
    return credit * cost_per_credit

# Path to the PDF file
pdf_path = r'C:\Users\Asus\Downloads\BSE_Student-Guidebook-2023-24.pdf'

# Extract tables from the PDF
tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

# Initialize list to hold processed data
data = []

# Process each table, skipping the first two tables
for i, table in enumerate(tables):
    if i < 2:
        continue  # Skip tables 1 and 2

    for index, row in table.iterrows():
        # Ensure the row has the expected structure
        if len(row) < 2:
            continue  # Skip rows that don't have at least two columns

        # Check if the cell is a string before stripping
        first_column = row[0]
        if isinstance(first_column, str):
            first_column = first_column.strip()
        else:
            continue  # Skip rows where the first column is not a string

        course_code = first_column.split()[0]

        # Validate the course code format (assuming course codes are alphanumeric and of a specific length)
        if not re.match(r'^[A-Z]{3}\d{4}$', course_code):
            continue  # Skip invalid course codes

        course_name = ' '.join(first_column.split()[1:])

        # Calculate credit value
        credit = calculate_credit(course_code)

        # Calculate cost
        cost = calculate_cost(credit)

        # Append the processed data to the list
        data.append([course_code, credit, cost])


# Create a DataFrame from the processed data
df = pd.DataFrame(data, columns=['Course', 'Credit', 'Cost'])

# Save the DataFrame to a CSV file
df.to_csv('courses.csv', index=False)

print(df)


# def extract_text_from_pdf(pdf_path):
#     document = fitz.open(pdf_path)
#     text_data = []
#     for page_num in range(len(document)):
#         page = document.load_page(page_num)
#         text = page.get_text("text")
#         text_data.append(text)
#     return text_data

# def parse_registration_info(text_data):
#     registration_info = {
#         "registration_date": [],
#         "course_code": [],
#         "fees": []
#     }

#     date_pattern = re.compile(r'Registration Date:\s*(\d{2}/\d{2}/\d{4})')
#     course_pattern = re.compile(r'\b(EEI|EEX|MHZ|CVM|DMM|EEM)\d{4}\b')
#     fees_pattern = re.compile(r'Rs\.?\s*([\d,]+) per credit')

#     fee_per_credit = 0

#     for page_text in text_data:
#         dates = date_pattern.findall(page_text)

#         courses_with_credits = course_pattern.findall(page_text)
#         course_codes = [course for course in courses_with_credits if course[1] in '3456']
#         credits = [int(course[1]) for course in courses_with_credits if course[1] in '3456']

#         fees_match = fees_pattern.search(page_text)
#         if fees_match:
#             fee_per_credit = int(fees_match.group(1).replace(',', ''))

#         total_fees = [credit * fee_per_credit for credit in credits]

#         max_length = max(len(dates), len(course_codes), len(total_fees))

#         dates.extend([None] * (max_length - len(dates)))
#         course_codes.extend([None] * (max_length - len(course_codes)))
#         total_fees.extend([None] * (max_length - len(total_fees)))

#         registration_info["registration_date"].extend(dates)
#         registration_info["course_code"].extend(course_codes)
#         registration_info["fees"].extend(total_fees)

#     return registration_info

# def save_to_csv(registration_info, output_path):
#     df = pd.DataFrame(registration_info)
#     df.to_csv(output_path, index=False)
#     print("Data extracted and saved successfully.")

# text_data = extract_text_from_pdf(pdf_path)

# registration_info = parse_registration_info(text_data)

# output_path = 'student_registration_data.csv'
# save_to_csv(registration_info, output_path)
