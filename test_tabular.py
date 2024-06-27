import tabula

pdf_path = r'C:\Users\Asus\Downloads\Student-Guidebook-engineering.pdf'
tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

print(f"Extracted {len(tables)} tables")
for i, table in enumerate(tables):
    print(f"Table {i + 1}")
    print(table)
