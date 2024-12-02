# Find Social Media Profiles on Other Platforms
For a given list of profiles on a single social media platform, parses Wikidata to extract social media profiles for a variety of other platforms

## Social Media Profile Extractor
This Python script extracts social media profiles from text using regular expressions. It can take in text as a command line argument or read from a CSV file containing a column named "text" and output a new CSV file containing the original text and a new column with extracted social media profiles.

### Usage
1. Run the script with the --text argument to extract social media profiles from a single string of text. Example:
    python script.py --text "TikTok: https://www.tiktok.com/test_test"
2. Run the script with the --csv_path argument to extract social media profiles from a CSV file. The script assumes that the CSV file has a column named "text" containing the text to parse. Example:
    python script.py --csv_path path/to/file.csv
3. The output CSV file will contain a new column named "social_media_profiles" with a dictionary of social media profiles extracted from the corresponding "text" column.
