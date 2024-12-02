import requests
import csv
import time

# API key and base parameters
base_params = {
    "api_key": "APIKEY",  # Replace with your actual API key
    "engine": "google",
    "location": "United States",
    "google_domain": "google.com",
    "gl": "us",
    "hl": "en",
    "start": "0",
    "num": "100"
}

countries = ["China", "Iran", "Russia"]
sites = ["instagram.com", "facebook.com", "youtube.com", "t.me", "tiktok.com", ]

def get_query(site, country):
    if site in ["instagram.com", "facebook.com", "threads.net"]:
        return f'"{country} state-controlled media" site:{site}'
    elif site == "tiktok.com":
        return f'"{country} state-affiliated media" site:{site}'
    elif site == "youtube.com":
        return f'"is funded in whole or in part by the {country} government." site:{site}'
    else:
        return ""

with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['country', 'site', 'title', 'link', 'snippet']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop over countries and sites
    for country in countries:
        for site in sites:
            query = get_query(site, country)
            if not query:
                continue  # Skip if query is empty
            print(f"Processing query: {query}")
            for start in range(0, 1000, 100):
                params = base_params.copy()
                params['q'] = query
                params['start'] = str(start)
                params['num'] = '100'
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
                    continue
                # Process the results
                if 'organic_results' in data and data['organic_results']:
                    for result in data['organic_results']:
                        # Get relevant fields
                        title = result.get('title', '')
                        link = result.get('link', '')
                        snippet = result.get('snippet', '')
                        # Write to CSV
                        writer.writerow({
                            'country': country,
                            'site': site,
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                else:
                    print(f"No more results for query: {query} starting at {start}")
                    break  # Exit the loop if no more results
                # Respect rate limits
                time.sleep(1)