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

text = '''During the Two Sessions, the government is expected to set its GDP growth target for 2023, which will surely receive added global attention, as China's recent reopening has paved the way for a faster-than-expected recovery. What kind of economic goals can be expected? Watch this video to unbox it.

Unboxing Two Sessions is a "box" of China's policy trends that we can expect to see at this year's Two Sessions, a key event on China's political calendar. This year's event will be the first one after the 20th National Congress of the Communist Party of China, marking a crucial year for marching toward Chinese modernization. In each episode, we choose an item and unbox it together.

For more: https://news.cgtn.com/news/2023-02-28...

Follow us on TikTok & Telegram
Streaming: https://www.epic-media.tv
TikTok: https://www.tiktok.com/epicmediachannel
Telegram: https://t.me/EpicMediaOfficial     
Ukraine's Got Talent on Facebook: https://www.facebook.com/UkraineGot
Ukraine's Got Talent on Instagram: https://www.instagram.com/UkraineGot
Subscribe to us on YouTube: https://goo.gl/lP12gA
Download our APP on Apple Store (iOS): https://itunes.apple.com/us/app/cctvn'''

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