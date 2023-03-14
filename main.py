import argparse
import pandas as pd
from social_profiler import extract_social_media_profiles
from config import CSV_PATH

# Create an ArgumentParser object to handle command line arguments
parser = argparse.ArgumentParser(description='Extract social media profiles from text')
parser.add_argument('--text', '-t', type=str, help='The text to extract social media profiles from', required=False)
parser.add_argument('--csv_path', '-c', type=str, help='A CSV file with at least one column named \'text\'', required=False)


# Parse the command line arguments
args = parser.parse_args()

text = '''TEST TEXT Lorem Ipsum
TikTok: https://www.tiktok.com/test_test
Telegram: https://t.me/Test     
Facebook: https://www.facebook.com/TEST
Instagram: https://www.instagram.com/@Test'''

if(args.text):
    # Set the description variable
    text = args.text
    print(extract_social_media_profiles(text))
else:
    # Override CSV if needed
    if(args.csv_path):
        CSV_PATH = args.csv_path

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(CSV_PATH)
    # Extract the descriptions from the DataFrame
    descriptions = df['text']

    # Parse the descriptions for social media profiles and add a new column to the DataFrame
    df['social_media_profiles'] = descriptions.apply(extract_social_media_profiles)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(CSV_PATH, index=False)