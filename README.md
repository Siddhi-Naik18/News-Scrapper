# Law News Scraping
## 📋 Project Overiew
This project is a web scraper that collects the latest news articles from Google News across categories like Sports, Entertainment, and Law. It uses requests and BeautifulSoup to gather article titles, snippets, and links. For detailed content, Selenium is employed to scrape each article. The project also integrates sentiment analysis to classify articles as positive, negative, or neutral based on their content.

## 📊 Key Features
- Web Scraping with requests and BeautifulSoup: Used the requests library to send HTTP requests and BeautifulSoup for parsing HTML content from Google News across multiple categories like Sports, Entertainment, Health, Technology, Business, and Law. 
- Article Collection: Extracted article titles and links, ensuring only the most recent articles are fetched. The number of articles fetched can be adjusted based on user preference.
- Selenium for Detailed Scraping: Utilized Selenium to scrape detailed article content for sentiment analysis.
- Sentiment Analysis with TextBlob: Used TextBlob for sentiment analysis to classify each article’s tone as positive, negative, or neutral.
- Summarization with Llama: Applied Llama from Hugging Face for summarizing entertainment articles, providing concise summaries, though the accuracy may not be perfect.
- Keyword Search: Implemented a search feature on the home page, allowing users to search for specific keywords and retrieve related news articles dynamically.
- Download Articles as CSV: Enabled users to download the fetched article titles and URLs (along with sentiment data) as a CSV file for further data analysis.
- Error Handling: Implemented exception handling to ensure smooth scraping even in case of missing or malformed elements.
- Dynamic Data Extraction: Enabled real-time data extraction with the ability to adjust search queries to fetch the latest news across various categories.

## 🚀 Getting Started
# Prerequisites
- Python 3.x

- Install the required libraries

``` 
pip install bs4
```

``` 
pip install textblob
```

``` 
pip install selenium
``` 
# Running the Project
1. Clone this repository:
```
git clone https://github.com/Siddhi-Naik18/News_Scrapper.git
```
2. Run the command to open streamlit app:
```
streamlit run .\1_??_Home.py
```

## 📂 Repository Structure
This repository contains the following files:
- 1_🏠_Home.py: File containing the Home page code.
- pages: Directory containing the Python files for each category.
- styles: Directory containing the style.css file.
- README.me: File provide with an overview of the project.

## 📸 Screenshots
![image](https://github.com/user-attachments/assets/5d738048-4d34-416d-909c-cb1e21afd713)

![image](https://github.com/user-attachments/assets/1b81de51-e658-4b7e-8ac6-99d46fe24ab6)

![image](https://github.com/user-attachments/assets/fc6c68b4-bc77-4c09-918e-f1cdb2b205a7)

![image](https://github.com/user-attachments/assets/39105bc4-3a35-4404-9ac5-2e839487bcef)

![image](https://github.com/user-attachments/assets/f1aea6b3-befc-4288-aa0c-c396b654d9ff)

![image](https://github.com/user-attachments/assets/9ec39838-aa83-4f8d-92e2-58ce133635a3)

![image](https://github.com/user-attachments/assets/3e29f3aa-2f3f-4a66-a3d0-f603fcbbd4a4)

## 📝 Conclusion
This project demonstrates the use of Python libraries for real-time news scraping, covering a variety of topics such as Sports, Entertainment, Health, Technology, Business, and Law. It provides an efficient way to collect and display news articles from Google News, along with sentiment analysis and summarization for better content understanding. The extracted data can be easily integrated into applications, making it a valuable resource for platforms requiring up-to-date news, such as news aggregators, custom dashboards, and applications in fields like sentiment analysis, market research, and content curation.

