import requests
import csv
import time
import urllib.parse
import pandas as pd

# API key and base parameters
base_params = {
    "api_key": "APIKEY",  # Replace with your actual SerpAPI key
    "engine": "google",
    "location": "United States",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "start": "0",
    "num": "20"
}

# Read the embassies from 'embassies.csv' using pandas
embassies_df = pd.read_csv('embassies.csv')

# List of sites to search
sites = ["instagram.com", "facebook.com", "youtube.com", "t.me", "tiktok.com", "x.com"]

def get_query(sites, embassy_name):
    site_query = ' OR '.join([f'site:{site}' for site in sites])
    return f'{embassy_name} ({site_query})'

# Prepare field names for the CSV file
embassy_columns = embassies_df.columns.tolist()
result_columns = ['site', 'title', 'link', 'snippet']
fieldnames = embassy_columns + result_columns

# Open the output CSV file
with open('results_embassies.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop over each embassy (row) in the DataFrame
    for index, row in embassies_df.iterrows():
        embassy_name = row['Name']
        query = get_query(sites, embassy_name)
        print(f"Processing query: {query}")
        for start in range(0, 10, 10):
            params = base_params.copy()
            params['q'] = query
            params['start'] = str(start)
            params['num'] = '10'
            try:
                response = requests.get('https://serpapi.com/search', params=params)
                data = response.json()
            except Exception as e:
                print(f"Error fetching results for query: {query} start: {start}")
                print(e)
                continue
            # Check for errors in the response
            if 'error' in data:
                print(f"Error in response for query: {query} start: {start}")
                print(data['error'])
                break  # Exit the loop if there's an error
            # Process the results
            if 'organic_results' in data and data['organic_results']:
                for result in data['organic_results']:
                    # Get relevant fields
                    title = result.get('title', '')
                    link = result.get('link', '')
                    snippet = result.get('snippet', '')
                    # Extract the site from the link
                    parsed_url = urllib.parse.urlparse(link)
                    site = parsed_url.netloc.replace('www.', '')
                    if site not in sites:
                        continue  # Skip sites not in our list
                    # Prepare the row data by combining embassy info and result info
                    row_data = row.to_dict()
                    row_data.update({
                        'site': site,
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                    # Write to CSV
                    writer.writerow(row_data)
            else:
                print(f"No more results for query: {query} starting at {start}")
                break  # Exit the loop if no more results
            # Respect rate limits
            time.sleep(1)