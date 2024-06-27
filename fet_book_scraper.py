import tabula
import pandas as pd
import re

# Function to calculate credit value from course code
def calculate_credit(course_code):
    try:
        # Extract the numeric part of the course code
        numeric_part = re.findall(r'\d+', course_code)[0]
        # The second digit of the numeric part represents the credit value
        credit_value = int(numeric_part[1])
        print(f"Course Code: {course_code}, Credit Value: {credit_value}")  # Log the credit value
        return credit_value
    except (IndexError, ValueError):
        # Return a default credit value or handle the error
        print(f"Course Code: {course_code}, Credit Value: 0 (Error)")  # Log the error
        return 0

# Function to calculate cost from credit value
def calculate_cost(course_code, credit):
    level = int(course_code[3])  # Get the starting digit of the numeric part
    if level in [3, 4]:
        cost_per_credit = 1980
    elif level in [5, 6, 7]:
        cost_per_credit = 3070
    else:
        cost_per_credit = 3990  # Default cost if level doesn't match specified levels
    return credit * cost_per_credit

# Path to the PDF file
pdf_path = r'C:\Users\Asus\Downloads\Student-Guidebook-engineering.pdf'


# Extract tables from the PDF
tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

# Initialize list to hold processed data
data = []

# Identify and process the curriculum table
for table in tables:
    df = pd.DataFrame(table)
    if 'Course' in df.columns and 'Prerequisite' in df.columns:
        for index, row in df.iterrows():
            course_code = row['Course'].split()[0]

            if not re.match(r'^[A-Z]{3}\d{4}$', course_code):
                continue

            credit = calculate_credit(course_code)
            cost = calculate_cost(course_code, credit)
            data.append([course_code, credit, cost])
    else:
        for index, row in df.iterrows():
            if len(row) < 2:
                continue

            first_column = row[0]
            if isinstance(first_column, str):
                first_column = first_column.strip()
            else:
                continue

            course_code = first_column.split()[0]

            if not re.match(r'^[A-Z]{3}\d{4}$', course_code):
                continue

            course_name = ' '.join(first_column.split()[1:])
            credit = calculate_credit(course_code)
            cost = calculate_cost(course_code, credit)
            data.append([course_code, credit, cost])

# Create a DataFrame from the processed data
df = pd.DataFrame(data, columns=['Course', 'Credit', 'Cost'])

# Save the DataFrame to a CSV file
output_path = 'D:/OUSL Final Project/chatbot_data_scraper/courses.csv'
df.to_csv(output_path, index=False)

print(df)
