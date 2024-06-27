import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Faculty of Engineering website
url = 'https://ou.ac.lk/fengtec/'  # Replace with the actual URL

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant data
    data = []
    info_elements = soup.find_all('div', class_='info_class')  # Replace with actual class or tag
    for elem in info_elements:
        title = elem.find('h3').text.strip()
        details = elem.find('p').text.strip()
        data.append([title, details])

    # Save data to a DataFrame
    df = pd.DataFrame(data, columns=['Title', 'Details'])

    # Save DataFrame to a CSV file
    df.to_csv('faculty_of_engineering_data.csv', index=False)
    print("Data scraped and saved successfully.")
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
