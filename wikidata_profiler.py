from wikidata.client import Client
import requests
import pandas as pd
import time
from io import StringIO

# Constants
URL_OR_CSV = "CSV"
CSV_FILE = "C:\\Users\\PeterBenzoni\\repo\\social_profiler\\Hamilton_Account_List2024.csv"
OUTPUT_FILE = "updated_domains_with_social_media.csv"

# Initialize the Wikidata client
client = Client()

# Mapping of Wikidata properties to their descriptions
social_media_properties = {
    'P2002':   'Twitter username',
    'P2013':   'Facebook ID',
    'P2003':   'Instagram username',
    'P2397':   'YouTube channel ID',
    'P7085':   'TikTok username',
    'P3789':   'Telegram username',
    'P11892':  'Threads username',
    'P11962':  'Rumble channel',
    'P3185':   'VK ID',
    'P8919':   'Gab username',
    'P9269':   'Odnoklassniki user numeric ID',
    'P8904':   'Parler username',
    'P10858':  'Truth Social username',
    # Add more properties as needed
}

# Mapping of your DataFrame columns to Wikidata properties
column_to_property = {
    'Twitter ID': 'P2002',
    'Facebook ID': 'P2013',
    'Instagram username': 'P2003',
    'YouTube channel ID': 'P2397',
    'TikTok username': 'P7085',
    'Telegram ID': 'P3789',
    'Threads username': 'P11892',
    'Rumble channel': 'P11962',
    'VK ID': 'P3185',
    'Gab username': 'P8919',
    'Odnoklassniki user numeric ID': 'P9269',
    'Parler username': 'P8904',
    'Truth Social username': 'P10858',
    # Add other mappings as needed
}

# Reverse mapping from property IDs to DataFrame columns
property_id_to_column = {v: k for k, v in column_to_property.items()}

def get_wikidata_id(property_id, value):
    sparql_query = f"""
        SELECT DISTINCT ?item WHERE {{
            ?item wdt:{property_id} "{value}".
        }}
        LIMIT 1
    """
    url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "YourAppName/1.0", 
        "Accept": "application/sparql-results+json"
    }
    try:
        response = requests.get(url, headers=headers, params={'query': sparql_query, 'format': 'json'})
        response_data = response.json()
        results = response_data.get('results', {}).get('bindings', [])

        if results:
            # Extract Wikidata ID from URI
            wikidata_uri = results[0]['item']['value']
            wikidata_id = wikidata_uri.split('/')[-1]
            return wikidata_id
    except Exception as e:
        print(f"Error fetching Wikidata ID for {value}: {e}")
        return None
    return None

def extract_social_media_profiles(data, social_media_properties):
    profiles = {}
    for prop_id, statements in data.items():
        if prop_id in social_media_properties:
            for statement in statements:
                if statement['mainsnak']['snaktype'] == 'value':
                    value = statement['mainsnak']['datavalue']['value']
                    profiles[prop_id] = value
    return profiles

def get_social_media_profiles_from_id(wikidata_id):
    try:
        item = client.get(wikidata_id, load=True)
        item_claims = item.data['claims']
        profiles = extract_social_media_profiles(item_claims, social_media_properties)
        return profiles
    except Exception as e:
        print(f"Error fetching profiles for {wikidata_id}: {e}")
        return None

def main():
    if URL_OR_CSV == "URL":
        response = requests.get(CSV_URL)
        decoded_content = response.content.decode('utf-8')
        df = pd.read_csv(StringIO(decoded_content))
    elif URL_OR_CSV == "CSV":
        df = pd.read_csv(CSV_FILE)
    else:
        print("Please set URL_OR_CSV to either 'URL' or 'CSV'")
        return
    
    # Ensure all required columns are present
    for column in column_to_property.keys():
        if column not in df.columns:
            df[column] = None
    
    # Add an 'updated' column
    if 'updated' not in df.columns:
        df['updated'] = None

    # Fetch social media profiles for each row
    for idx, row in df.iterrows():
        wikidata_id = None
        # First, try to find the Wikidata ID using available social media usernames
        for column, property_id in column_to_property.items():
            if pd.notnull(row.get(column)) and row[column]:
                value = str(row[column]).strip()
                if not wikidata_id:
                    wikidata_id = get_wikidata_id(property_id, value)
                    if wikidata_id:
                        print(f"Found Wikidata ID {wikidata_id} for {value} in column {column}")
                        break  # Stop after finding the first valid Wikidata ID

        if wikidata_id:
            profiles = get_social_media_profiles_from_id(wikidata_id)
            if profiles:
                for prop_id, profile_value in profiles.items():
                    if prop_id in property_id_to_column:
                        column_name = property_id_to_column[prop_id]
                        if pd.isnull(row.get(column_name)) or not row[column_name]:
                            df.at[idx, column_name] = profile_value
                            df.at[idx, 'updated'] = True
        else:
            print(f"No Wikidata ID found for row {idx}")
        time.sleep(0.5)  # Avoid hitting API rate limits

    # Save the updated data to a new CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Updated data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()