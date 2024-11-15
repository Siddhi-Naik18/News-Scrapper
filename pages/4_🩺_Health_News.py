import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from textblob import TextBlob

def get_sentiment(article_text):
    blob = TextBlob(article_text)
    polarity = blob.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)
    if polarity > 0:
        return "POSITIVE", polarity
    elif polarity < 0:
        return "NEGATIVE", polarity
    else:
        return "NEUTRAL", polarity

def get_health_news():
# URL for the website
    url = 'https://news.google.com/search?q=health&hl=en-IN&gl=IN&ceid=IN%3Aen'
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all main li elements
    main_tags = soup.find_all('c-wiz', class_='PO9Zff Ccj79 kUVvS')

    # driver = init_selenium()  # Initialize Selenium driver here
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless to avoid opening a browser window
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver  = webdriver.Chrome()

    # List to store the news articles
    newslist = []
    count = 0

    for item in main_tags:
        if count >= limit:
            break
        try:
            # Find the div with class 'col-sm-8 col-lg-8 brief'
            brief_div = item.find('div', class_='IL9Cne')
            if brief_div:
                # Find the h4 tag within this div
                a_tag = brief_div.find('a')
                
                if a_tag:
                    title = a_tag.get_text(strip=True)
                    link = "https://news.google.com" + a_tag['href'][1:]

                    # Use Selenium to fetch article content
                    driver.get(link)
                    driver.implicitly_wait(5)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    p_texts = [p.get_text(strip=True) for p in soup.find_all('p')]
                    br_texts = [br.get_text(strip=True) for br in soup.find_all('br')]
                    h2_texts = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
                    div_texts = [div.get_text(strip=True) for div in soup.find_all('div')]

                    
                    full_text = f'{title}. ' + " ".join(h2_texts + br_texts + div_texts + p_texts)
                    # summary = get_summary(full_text) or "summary not available"
                    sentiment = get_sentiment(full_text)

                    newsarticle = {
                        'title': a_tag.get_text(strip=True),
                        'link': "https://news.google.com" +a_tag['href'],
                        'sentiment': sentiment
                    }
                    newslist.append(newsarticle)
                    count += 1
        except Exception as e:
            print(f"Error: {e}")
            
    driver.quit()  # Close the Selenium driver after scraping
    return newslist


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def convert_to_csv(newslist):
    # Create a pandas DataFrame
    df = pd.DataFrame(newslist)
    # Convert the DataFrame to CSV format
    return df.to_csv(index=False).encode('utf-8')

# # Load the external CSS
css_path = pathlib.Path("styles/style.css")
load_css(css_path)


st.title("🩺 Health News Scraper")

limit = st.number_input("How many articles would you like to scrape?", min_value=1, max_value=100, value=10, step=1)

if st.button("Get Health News", key="submit"):
    news = get_health_news()

    if news:
        for article in news:
            st.subheader(article["title"])
            st.write(f"**Sentiment**: {article['sentiment']}")
            st.write(f"[Read more]({article['link']})")

        csv_data = convert_to_csv(news)

        # Provide the download link for the CSV file
        st.download_button(
            key="download",
            label="Download as CSV",
            data=csv_data,
            file_name='health_news.csv',
            mime='text/csv',
        )

    else:
        st.write("No articles found")


