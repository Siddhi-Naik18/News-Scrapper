import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from textblob import TextBlob


# Configure Hugging Face API for summarization
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
headers = {"Authorization": "Bearer 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"} 

# Summarize function using Hugging Face API
def get_summary(text, retries = 3):
    prompt = f"Summarize the following article in one or two sentences:\n\n{text}\n\nSummary:"
    payload = {"inputs": prompt}

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            summary = response.json()
            if isinstance(summary, list) and summary:
                summary = summary[0].get('generated_text', "Summary not available")
            else:
                summary = "Summary not available"        
            return summary
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            if attempt < retries - 1:
                continue  # Retry if attempts remain
            else:
                return "Summary not available"
            

def get_sentiment(article_text):
    blob = TextBlob(article_text)
    polarity = blob.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)
    if polarity > 0:
        return "POSITIVE", polarity
    elif polarity < 0:
        return "NEGATIVE", polarity
    else:
        return "NEUTRAL", polarity

# Function to scrape news and get content from `<p>` and `<br>` tags
def get_entertain_news(limit):
    url = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_tags = soup.find_all('c-wiz', class_='PO9Zff Ccj79 kUVvS')
    
    # driver = init_selenium()  # Initialize Selenium driver here
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless to avoid opening a browser window
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver  = webdriver.Chrome()

    newslist = []
    count = 0

    for item in main_tags:
        if count >= limit:
            break
        try:
            article_tag = item.find('article', class_='IBr9hb')
            if article_tag:
                a_tag = article_tag.find('a', class_='gPFEn')
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

                    
                    full_text = f'{title}. ' + " ".join(div_texts + br_texts + h2_texts + p_texts)
                    summary = get_summary(full_text) or "summary not available"
                    sentiment = get_sentiment(full_text)

                    newsarticle = {
                        'title': title,
                        'link': link,
                        'summary': summary or "Summary not available",
                        'sentiment': sentiment
                    }
                    newslist.append(newsarticle)
                    count += 1
        except Exception as e:
            st.write(f"Error: {e}")

    driver.quit()  # Close the Selenium driver after scraping
    return newslist

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Convert news list to CSV
def convert_to_csv(newslist):
    df = pd.DataFrame(newslist)
    return df.to_csv(index=False).encode('utf-8')

# # Load the external CSS
css_path = pathlib.Path("styles/style.css")
load_css(css_path)

# Streamlit app interface
st.title("🎭 Entertainment News Scraper")

limit = st.number_input("How many articles would you like to scrape?", min_value=1, max_value=100, value=10, step=1)

if st.button("Get Entertainment News", key="submit"):
    news = get_entertain_news(limit)

    if news:
        for article in news:
            st.subheader(article["title"])
            st.write(f"**Summary**: {article['summary']}")
            st.write(f"**Sentiment**: {article['sentiment']}")
            st.write(f"[Read more]({article['link']})")

        csv_data = convert_to_csv(news)

        # Provide download button for the CSV file
        st.download_button(
            key="download",
            label="Download as CSV",
            data=csv_data,
            file_name='entertainment_news.csv',
            mime='text/csv',
        )
    else:
        st.write("No articles found")

