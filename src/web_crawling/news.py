from bs4 import BeautifulSoup
import requests
from openai import OpenAI
import sys
import json
import time

client = OpenAI(api_key = "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", organization = "org-wtrrt7KeUZ4jD9BpsDIGnpd2")
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75" }

espn_home = "https://www.espn.com"


# ESPN 크롤링
url = espn_home + "/tennis/"
original_html = requests.get(url, headers=headers)
# set time out 1 s
time.sleep(1.0)

html = BeautifulSoup(original_html.text, "html.parser")

articles = html.find_all("article", attrs={"class":"contentItem"})

article_count = 0

article_array = []
for context in articles:
    try:
        art_url = espn_home + context.find("a", attrs={"class":"contentItem__padding"})["href"]
        time.sleep(0.3)
        news_html = requests.get(art_url, headers=headers)
        bs_news = BeautifulSoup(news_html.text, "html.parser")
        title = bs_news.find("header", attrs={"class":"article-header"}).contents[0].text
        if(len(title) > 48):
            title = title[:48]
            title += "..."
            
        date = bs_news.find("span", attrs={"class":"timestamp"})
        image = context.find("img", attrs={"class":"media-wrapper_image"})["data-default-src"]
        if len(image) == 0:
            image = "../../images/icons.ico/logo_512x512.png"

        body = bs_news.find("div", attrs={"class":"article-body"})
        body_content = body.find_all("p")
        body_contents = "\n".join(content.text for content in body_content)
        article = title + "\n" + body_contents
        prompt = f"{article}\nSummrize this article shortly (under 135 character if possible & just a plain text)."
        response = client.completions.create(
            model = "gpt-3.5-turbo-instruct-0914",
            prompt = prompt,
            max_tokens = 500
        )


        if(len(response.choices[0].text) > 135):
            response = response[:135]
            response += "..."

        if not (len(title) == 0 and len(response.choices[0].text) == 0 and len(art_url) == 0):
            article_array.append({"title":title, "img":image, "response": response.choices[0].text, "url":art_url})
            # print(f"{title}\n{response.choices[0].text}\n==================================================\n")
            article_count = article_count+1
    except:
        print("\n")

article_json = json.dumps(article_array)
print(article_json)
sys.stdout.flush()
