import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing provider details
        table = soup.find('table')

        # Check if the table is found
        if table:
            # Initialize lists to store data
            names = []
            titles = []
            genders = []
            expertise = []
            research_interests = []
            phones = []
            locations = []
            educations = []

            # Loop through rows in the table
            for row in table.find_all('tr')[1:]:  # Skip the header row
                columns = row.find_all('td')
                names.append(columns[0].text.strip())
                titles.append(columns[1].text.strip())
                genders.append(columns[2].text.strip())
                expertise.append(columns[3].text.strip())
                research_interests.append(columns[4].text.strip())
                phones.append(columns[5].text.strip())
                locations.append(columns[6].text.strip())
                educations.append(columns[7].text.strip())

            # Create a DataFrame
            data = {
                'Name': names,
                'Title': titles,
                'Gender': genders,
                'Expertise': expertise,
                'Research Interests': research_interests,
                'Phone': phones,
                'Location': locations,
                'Education': educations
            }
            df = pd.DataFrame(data)

            return df
        else:
            print("Error: Table not found on the webpage.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to retrieve data. {e}")
        return None

# URL of the webpage
url = 'https://intake.steerhealth.io/doctor-search/aa1f8845b2eb62a957004eb491bb8ba70a'

# Scrape data
df = scrape_data(url)

# Check if data is retrieved successfully
if df is not None:
    # Save data to CSV
    df.to_csv('provider_details.csv', index=False)

    # Display the first few rows of the DataFrame
    print(df.head())