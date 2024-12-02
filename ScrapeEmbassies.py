import pandas as pd
import time
import random
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Function to check for 403 errors and prompt user
def check_response(status):
    if status == 403:
        user_input = input("Received a 403 Forbidden error. Do you want to continue? (yes/no): ")
        if user_input.lower() != 'yes':
            print("Exiting script.")
            exit()
        else:
            print("Continuing script.")

def main():
    base_url = 'https://www.embassypages.com'
    data = []
    target_countries = ['China', 'Iran', 'Russia']

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the main page
        try:
            page.goto(base_url, timeout=60000)
            print("Accessed main page.")
        except PlaywrightTimeoutError:
            print("Timeout while accessing the main page.")
            return

        # Get the list of countries
        countries = page.query_selector_all('ul.country-list li a')
        country_urls = []
        for country in countries:
            country_name = country.inner_text()
            country_href = country.get_attribute('href')
            country_url = country_href if country_href.startswith('http') else base_url + '/' + country_href.lstrip('/')
            country_urls.append((country_name, country_url))

        # Loop over each country
        for idx, (country_name, country_url) in enumerate(country_urls):
            print(f'Processing country: {country_name} ({idx +1}/{len(country_urls)})')
            try:
                page.goto(country_url, timeout=60000)
                if page.response.status == 403:
                    check_response(403)

                # Random delay
                time.sleep(random.uniform(2, 5))

                # Find the list of embassies/consulates
                embassies = page.query_selector_all('ul.letter-block__list-ec li a')

                if not embassies:
                    continue  # Skip if no embassies are listed

                for embassy in embassies:
                    embassy_name = embassy.inner_text()
                    embassy_href = embassy.get_attribute('href')
                    embassy_url = embassy_href if embassy_href.startswith('http') else base_url + '/' + embassy_href.lstrip('/')

                    # Check if the embassy is from China, Iran, or Russia
                    if any(target_country in embassy_name for target_country in target_countries):
                        print(f'Found embassy: {embassy_name}')
                        try:
                            page.goto(embassy_url, timeout=60000)
                            if page.response.status == 403:
                                check_response(403)

                            # Random delay
                            time.sleep(random.uniform(2, 5))

                            # Extract social media links
                            social_media_links = []
                            social_media_div = page.query_selector('div.social__media.embassy-mission__link')
                            if social_media_div:
                                social_links = social_media_div.query_selector_all('a')
                                for link in social_links:
                                    href = link.get_attribute('href')
                                    social_media_links.append(href)

                            # Extract website links
                            website_links = []
                            website_div = page.query_selector('div.website')
                            if website_div:
                                website_links_list = website_div.query_selector_all('a')
                                for link in website_links_list:
                                    href = link.get_attribute('href')
                                    website_links.append(href)

                            # Extract the embassy type and city from the name
                            embassy_info = embassy_name.split(',')
                            if len(embassy_info) >= 2:
                                embassy_country = embassy_info[0].strip()
                                city_and_type = embassy_info[1].strip()
                                city_and_type_parts = city_and_type.split(' - ')
                                embassy_city = city_and_type_parts[0].strip()
                                if len(city_and_type_parts) > 1:
                                    embassy_type = city_and_type_parts[1].strip()
                                else:
                                    embassy_type = ''
                            else:
                                embassy_country = embassy_name.strip()
                                embassy_city = ''
                                embassy_type = ''

                            # Append data
                            data.append({
                                'Host Country': country_name,
                                'Embassy Country': embassy_country,
                                'Embassy City': embassy_city,
                                'Embassy Type': embassy_type,
                                'Social Media Links': ', '.join(social_media_links),
                                'Website Links': ', '.join(website_links),
                                'Embassy Page URL': embassy_url
                            })

                        except PlaywrightTimeoutError:
                            print(f'Timeout while accessing embassy {embassy_name}')
                            continue
            except PlaywrightTimeoutError:
                print(f'Timeout while accessing country {country_name}')
                continue

        # Close the browser
        browser.close()

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(data)
    df.to_excel('embassies_social_media.xlsx', index=False)
    print("Data saved to 'embassies_social_media.xlsx'.")

if __name__ == '__main__':
    main()