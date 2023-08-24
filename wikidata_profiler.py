from wikidata.client import Client

import requests
import pandas as pd
import time
import tldextract
from io import StringIO

URL_OR_CSV = "URL"
CSV_FILE = "State_Media_Matrix.csv"
CSV_URL = "https://raw.githubusercontent.com/ASD-at-GMF/state-media-profiles/main/State_Media_Matrix.csv"
COLUMN = "URL"
WIKIDATA_URL = "https://www.wikidata.org/w/api.php"
WIKIDATA_ID = 'P856'
OUTPUT_FILE = "updated_domains_with_social_media.csv"

social_media_properties = {
    'P553':    'website account on',
    'P856':    'Official Website',
    'P554':    'website username or ID',
    'P998':    'Curlie ID',
    'P1997':   'Facebook Places ID',
    'P2002':   'Twitter username',
    'P2003':   'Instagram username',
    'P2013':   'Facebook ID',
    'P2037':   'GitHub username',
    'P2397':   'YouTube channel ID',
    'P2847':   'Google+ ID',
    'P2942':   'Dailymotion channel ID',
    'P2984':   'Snapchat username',
    'P3040':   'SoundCloud ID',
    'P3185':   'VK ID',
    'P3207':   'Vine user ID',
    'P3258':   'LiveJournal ID',
    'P3265':   'Myspace ID',
    'P3267':   'Flickr user ID',
    'P3417':   'Quora topic ID',
    'P3502':   'Ameblo username',
    'P3579':   'Sina Weibo user ID',
    'P3789':   'Telegram username',
    'P3836':   'Pinterest username',
    'P3899':   'Medium username',
    'P3943':   'Tumblr username',
    'P3984':   'subreddit',
    'P4003':   'Facebook page ID',
    'P4013':   'Giphy username',
    'P4015':   'Vimeo ID',
    'P4016':   'SlideShare username',
    'P4017':   'Ustream username',
    'P4033':   'Mastodon address',
    'P4073':   'Fandom wiki ID',
    'P4173':   'Instagram location ID',
    'P4174':   'Wikimedia username',
    'P4175':   'Patreon ID',
    'P4226':   'Cyworld ID',
    'P4264':   'LinkedIn organization ID',
    'P4265':   'Reddit username',
    'P4411':   'Quora username',
    'P5163':   'Odnoklassniki ID',
    'P5434':   'Gfycat user ID',
    'P5435':   'pixiv user ID',
    'P5797':   'Twitch channel ID',
    'P5933':   'Twitter post ID',
    'P6450':   'Douban username',
    'P6451':   'Zhihu username',
    'P6455':   'Bilibili user ID',
    'P6459':   'QQ user ID',
    'P6552':   'Twitter numeric user ID',
    'P6634':   'LinkedIn personal profile ID',
    'P6654':   'Periscope ID',
    'P6837':   'Keybase username',
    'P6900':   'NicoNicoPedia ID',
    'P7085':   'TikTok username',
    'P7120':   'Douyin ID',
    'P7171':   'Hacker News username',
    'P7211':   'Line Blog user ID',
    'P7590':   'eBay username',
    'P7737':   'DeviantArt username',
    'P8827':   'GitLab.com username',
    'P8842':   'PromoDj ID',
    'P8904':   'Parler username',
    'P8919':   'Gab username',
    'P8976':   'Lichess username',
    'P9101':   'Discord username',
    'P9269':   'Odnoklassniki user numeric ID',
    'P9271':   'Kickstarter username',
    'P9345':   'Discord server numeric ID',
    'P9509':   'Mixcloud ID',
    'P9675':   'MediaWiki page ID',
    'P9694':   'VK Music artist ID',
    'P9812':   'Likee username',
    'P9819':   'Daum Cafe ID',
    'P9928':   'Baijiahao ID',
    'P9934':   'Zenodo communities ID',
    'P10027':  'official forum URL',
    'P10048':  'Meetup group id',
    'P10152':  'Rutube channel ID',
    'P10208':  'Coub channel ID',
    'P10230':  'Viber group ID',
    'P10352':  'Naver TV ID',
    'P10477':  'ICQ user ID',
    'P10557':  'Zotero ID',
    'P10558':  'My World@Mail.Ru ID',
    'P10858':  'Truth Social username',
    'P10884':  'Gitee username',
    'P10922':  'TamTam chat ID',
    'P10924':  'Mozilla Hacks author ID',
    'P10990':  'YAPPY profile ID',
    'P11036':  'Instagram post ID',
    'P11245':  'YouTube handle',
    'P11337':  'Twitter community ID',
    'P11559':  'TikTok place ID',
    'P11625':  'Spotify user ID',
    'P11705':  'Facebook numeric ID',
    'P11713':  'Patreon user numeric ID',
    'P11892':  'Threads username',
    'P11898':  'Stage 32 profile ID',
    'P11947':  'Lemmy community ID',
    'P11962':  'Rumble channel',
    'P963':    'streaming media URL',
    'P1902':   'Spotify artist ID',
    'P2397':   'YouTube channel ID',
    'P2722':   'Deezer artist ID',
    'P2942':   'Dailymotion channel ID',
    'P3283':   'Bandcamp profile ID',
    'P4015':   'Vimeo ID',
    'P4017':   'Ustream username',
    'P7085':   'TikTok username',
    'P10990':  'YAPPY profile ID',
    'P11245':  'YouTube handle',
    'P11962':  'Rumble channel',
    'P5797':   'Twitch channel ID',
    'P4175':   'Patreon ID',
    'P7953':   'Indiegogo project ID',
    'P8019':   'Kickstarter project ID',
    'P9271':   'Kickstarter username',
    'P11713':  'Patreon user numeric ID'
}
# Initialize the Wikidata client
client = Client()


# Define a function to get the Wikidata item ID for a domain


def get_wikidata_id(wikiValue):
    sparql_query = f"""
        SELECT DISTINCT ?item ?itemLabel WHERE {{
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
            {{
                SELECT DISTINCT ?item WHERE {{
                    ?item p:{WIKIDATA_ID} ?statement0.
                    ?statement0 (ps:{WIKIDATA_ID}) <{wikiValue}>.
                }}
                LIMIT 100
            }}
        }}
    """
    
    
    url = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "AS-at-GMF/1.0", 
        "Accept": "application/sparql-results+json"
    }
    
    response = requests.get(url, headers=headers, params={'query': sparql_query, 'format': 'json'})
    response_data = response.json()
    results = response_data.get('results', {}).get('bindings', [])

    if results and len(results) > 0:
        # Extract Wikidata ID from URI
        wikidata_uri = results[0]['item']['value']
        wikidata_id = wikidata_uri.split('/')[-1]
        return wikidata_id
    return None

# Define a function to extract the social media profiles from the JSON data
def extract_social_media_profiles(data, social_media_properties):
    profiles = {}
    for prop_id, platform in social_media_properties.items():
        if prop_id in data:
            profiles[platform] = []
            for statement in data[prop_id]:
                if statement['mainsnak']['snaktype'] == 'value':
                    value = statement['mainsnak']['datavalue']['value']
                    profiles[platform]= value
    print(profiles)
    return profiles

# Define a function to get the social media profiles for a Wikidata item ID


def get_social_media_profiles(domains_to_check):
    try:
        wikidata_id = None
        for domain in domains_to_check:
            wikidata_id = get_wikidata_id(domain)
            if wikidata_id:
                break
        if not wikidata_id:
            return None
        item = client.get(wikidata_id, load=True)
        item_claims = item.data['claims']
        profiles = extract_social_media_profiles(item_claims, social_media_properties)
        return profiles
    except Exception as e:
        print(domain, e.args[0])
        return None

def extract_possible_domains(url):
    extracted = tldextract.extract(url)
    domains = [
        url,
        "https://" + '.'.join(part for part in (extracted.subdomain, extracted.domain, extracted.suffix) if part) + "",
        "https://" + '.'.join(part for part in (extracted.subdomain, extracted.domain, extracted.suffix) if part) + "/",
        "http://" + '.'.join(part for part in (extracted.subdomain, extracted.domain, extracted.suffix) if part) + "",
        "https://www." + '.'.join(part for part in (extracted.domain, extracted.suffix) if part) + "/", 
        "http://www." + '.'.join(part for part in (extracted.domain, extracted.suffix) if part) + "",

        '.'.join(part for part in (extracted.subdomain, extracted.domain, extracted.suffix) if part)
        ]    # combine the subdomain, domain, and suffix (TLD) to get the full domain
    return domains

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
    
    
    # Add columns for social media profiles
    df = df.assign(**{c: None for c in social_media_properties.values()})


    # Fetch social media profiles for each domain and add to the data
    for idx, row in df.iterrows():
        domain = row[COLUMN]
        if pd.isna(domain):
            continue    
        print(domain)

        if COLUMN != 'URL':
            profiles = get_social_media_profiles(domain)
        
        profiles = get_social_media_profiles(extract_possible_domains(domain))
        if profiles is not None:
            for platform, profile in profiles.items():
                df.at[idx, platform] = profile


        time.sleep(1)  # Adding a delay to avoid hitting the API rate limits

    # Save the updated data to a new CSV
    df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    main()