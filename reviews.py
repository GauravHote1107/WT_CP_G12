from typing import Dict, List, Union

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from textblob import TextBlob

nltk.download("stopwords")

custom_headers = {
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
        " Version/17.1 Safari/605.1.15"
    ),
}

session = requests.Session()
session.headers = custom_headers


def get_soup(url: str) -> Union[BeautifulSoup, None]:
    response = session.get(url)
    if response.status_code != 200:
        print("Error in getting webpage")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_comments(soup: BeautifulSoup) -> List[Dict[str, Union[str, int]]]:
    review_elements = soup.select("div.review")
    scraped_comments = []
    for review in review_elements:
        r_content_element = review.select_one("span.review-text")
        r_rating_element = review.select_one("i.a-icon-star")
        r_content = r_content_element.text.strip() if r_content_element else None
        r_rating = r_rating_element.text.strip() if r_rating_element else None
        if r_content:
            scraped_comments.append({"content": r_content, "rating": r_rating})

    return scraped_comments


def get_words_count(comments: List[str]) -> List[Dict[str, Union[str, int]]]:
    text = " ".join(comment["content"] for comment in comments)
    stop_words = set(stopwords.words("english"))
    word_tokens = text.split()

    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    filtered_set = set(filtered_text)

    return [
        {"x": text, "value": count}
        for text in filtered_set
        if (count := filtered_text.count(text)) >= 2
    ]


def analyze_sentiment(comment: str) -> str:
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"
