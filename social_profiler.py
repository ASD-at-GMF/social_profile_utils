import re

# The given text
description = "TEST"
social_media_regex = {
     "Facebook": r"https?://(?:www\.)?facebook\.com/([^/?]+)",
    "YouTube": r"https?://(?:www\.)?youtube\.com/(?:user|channel)/([^/?]+)",
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
    "Locals": r"https?://(?:www\.)?locals\.com/([\w.-]+)",
    "Apple Podcasts": r"https?://(?:podcasts\.apple\.com|itunes\.apple\.com)/([^/?]+)",
    "iHeartRadio": r"https?://(?:www\.)?iheart\.com/(?:[^/]+/)?(?:podcast|show)/([\w-]+)",
    "Google Play": r"https?://play\.google\.com/store/apps/details\?id=([\w.]+)"
    # "Other Website": r"https?://(www\.)?[a-zA-Z0-9]+\.[a-zA-Z]+(/[^\s]*)?"
    # Add more social media platforms and their regular expressions as needed
}

def extract_social_media_profiles(text_to_parse): 
    # A dictionary to store the extracted social media profiles
    social_media_profiles = {}
    # Loop through the social media platforms and extract the profiles
    if(isinstance(text_to_parse, str) and len(text_to_parse) > 5):
        for platform, regex in social_media_regex.items():
                matches = re.findall(regex, text_to_parse)
                for i in range(len(matches)):
                    matches[i] = matches[i].split('\r')[0].split('\n')[0]
                if matches:
                    social_media_profiles[platform] = matches
    return social_media_profiles

