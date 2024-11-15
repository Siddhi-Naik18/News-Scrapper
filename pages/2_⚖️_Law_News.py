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

# Function to scrape Google News for law-related articles
def get_law_news():
    # URL for the Google News search query
    url = 'https://news.google.com/search?q=law&hl=en-IN&gl=IN&ceid=IN%3Aen'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article elements
    articles = soup.find_all('article')

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

    for item in articles:
        if count >= limit:
            break
        try:
            # Find the title element using the class 'JtKRv'
            title_elem = item.find(class_='JtKRv')
            # Find the link element
            link_elem = item.find('a', href=True)

            if title_elem and link_elem:
                title = title_elem.get_text(strip=True)
                link = "https://news.google.com" + link_elem['href'][1:]

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
                    'title': title,
                    'link': link,
                    'sentiment': sentiment
                }
                newslist.append(newsarticle)
                count += 1
        except Exception as e:
            st.error(f"Error: {e}")

    driver.quit()  # Close the Selenium driver after scraping
    return newslist

# Streamlit app to display the news articles
st.title("⚖️ Law News Scraper")

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def convert_to_csv(newslist):
    # Create a pandas DataFrame
    df = pd.DataFrame(newslist)
    # Convert the DataFrame to CSV format
    return df.to_csv(index=False).encode('utf-8')

# Load the external CSS
css_path = pathlib.Path("styles/style.css")
load_css(css_path)

limit = st.number_input("How many articles would you like to scrape?", min_value=1, max_value=100, value=10, step=1)

# Button to trigger the scraping
if st.button("Scrape Law News", key = "submit"):
    news = get_law_news()

    # Display the articles if any are found
    if news:
        for article in news:
            st.subheader(article['title'])
            st.write(f"**Sentiment**: {article['sentiment']}")
            st.write(f"[Read more]({article['link']})")

        csv_data = convert_to_csv(news)

        st.download_button(
            key="download",
            label="Download as CSV",
            data=csv_data,
            file_name='law_news.csv',
            mime='text/csv',
        )
    else:
        st.write("No articles found.")

