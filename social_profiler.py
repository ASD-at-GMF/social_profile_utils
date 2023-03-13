import re

# The given text
description = '''During the Two Sessions, the government is expected to set its GDP growth target for 2023, which will surely receive added global attention, as China's recent reopening has paved the way for a faster-than-expected recovery. What kind of economic goals can be expected? Watch this video to unbox it.

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
social_media_regex = {
     "Facebook": r"https?://(?:www\.)?facebook\.com/([^/?]+)",
    "YouTube": r"https?://(?:www\.)?youtube\.com/(?:user|channel)/([^/?]+)",
    "WhatsApp": r"(\+?\d{1,3}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
    "Instagram": r"https?://(?:www\.)?instagram\.com/(@?[\w.-]+)",
    "TikTok": r"https?://(?:www\.)?tiktok\.com/(@?[\w.-]+)",
    "LinkedIn": r"https?://(?:www\.)?linkedin\.com/in/([\w-]+)",
    "Telegram": r"https?://(?:www\.)?t\.me/([\w-]+)",
    "Douyin": r"https?://(?:www\.)?douyin\.com/(@?[\w.-]+)",
    "QQ": r"https?://user\.qzone\.qq\.com/(\d+)",
    "Snapchat": r"https?://(?:www\.)?snapchat\.com/add/([\w.-]+)",
    "Pinterest": r"https?://(?:www\.)?pinterest\.com/([^/?]+)",
    "Reddit": r"https?://(?:www\.)?reddit\.com/user/([\w-]+)",
    "Twitter": r"https?://(?:www\.)?twitter\.com/([\w-]+)",
    "imo": r"https?://(?:www\.)?imo\.im/([\w.-]+)",
    "Line": r"https?://(?:www\.)?line\.me/R/ti/p/([\w.-]+)",
    "Vevo": r"https?://(?:www\.)?vevo\.com/([^/?]+)",
    "Discord": r"https?://(?:www\.)?discord(?:app)?\.com/([\w.-]+)",
    "Twitch": r"https?://(?:www\.)?twitch\.tv/([\w.-]+)",
    "VK": r"https?://(?:www\.)?vk\.com/([\w.-]+)",
    "Parler": r"https?://(?:www\.)?parler\.com/profile/([\w.-]+)",
    "Gab": r"https?://(?:www\.)?gab\.com/([\w.-]+)",
    "Odysee": r"https?://(?:www\.)?odysee\.com/(@?[\w.-]+)",
    "LBRY": r"https?://(?:www\.)?lbry\.tv/(@?[\w.-]+)",
    "Truth Social": r"https?://(?:www\.)?truthsocial\.com/user/([\w.-]+)",
    "BitChute": r"https?://(?:www\.)?bitchute\.com/channel/([\w.-]+)",
    "Gettr": r"https?://(?:www\.)?gettr\.com/user/([\w.-]+)",
    "Rumble": r"https?://(?:www\.)?rumble\.com/([\w.-]+)",
    # "iTunes": r"https?://(?:itunes\.apple\.com|apps\.apple\.com)/([^/?]+)",
    # "Google Play": r"https?://play\.google\.com/store/apps/details\?id=([\w.]+)",
    # "Other Website": r"https?://(www\.)?[a-zA-Z0-9]+\.[a-zA-Z]+(/[^\s]*)?"
    # Add more social media platforms and their regular expressions as needed
}

def extract_social_media_profiles(description): 
    # A dictionary to store the extracted social media profiles
    social_media_profiles = {}
    # Loop through the social media platforms and extract the profiles
    for platform, regex in social_media_regex.items():
        matches = re.findall(regex, description)
        if matches:
            social_media_profiles[platform] = matches
            print(platform, matches)
    return social_media_profiles

