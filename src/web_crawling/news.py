from bs4 import BeautifulSoup
import requests
from openai import OpenAI

client = OpenAI(api_key = "blank", organization = "org-wtrrt7KeUZ4jD9BpsDIGnpd2")
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75" }

espn_home = "https://www.espn.com"


# ESPN 크롤링
url = espn_home + "/tennis/"
original_html = requests.get(url, headers=headers)
html = BeautifulSoup(original_html.text, "html.parser")

articles = html.find_all("article", attrs={"class":"contentItem"})

article_count = 0
for context in articles:
    try:
        art_url = espn_home + context.find("a", attrs={"class":"contentItem__padding"})["href"]
        news_html = requests.get(art_url, headers=headers)
        bs_news = BeautifulSoup(news_html.text, "html.parser")
        title = bs_news.find("header", attrs={"class":"article-header"}).contents[0].text
        body = bs_news.find("div", attrs={"class":"article-body"})
        body_content = body.find_all("p")
        body_contents = "\n".join(content.text for content in body_content)
        article = title + "\n" + body_contents
        prompt = f"{article}\nSummrize this article shortly."
        response = client.completions.create(
            model = "gpt-3.5-turbo-instruct-0914",
            prompt = prompt,
            max_tokens = 500
        )
        print(f"{title}\n{response.choices[0].text}\n==================================================\n")
        article_count = article_count+1
    except:
        print("\n")
