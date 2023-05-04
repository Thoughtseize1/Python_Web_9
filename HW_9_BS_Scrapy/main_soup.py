import json
import os


import requests
from bs4 import BeautifulSoup

current_directory = os.path.dirname(os.path.abspath(__file__))
base_url = "https://quotes.toscrape.com"
authors = []
qoutes = []


def write_to_json(name_of_file: str, data):
    file_path = os.path.join(current_directory, name_of_file + ".json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def grab_autrhor_biography(session, page_url):
    response = session.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    birthday_date = soup.select("span[class=author-born-date]")[0].text
    description = soup.select("div[class=author-description]")[0].text

    born_location = soup.select("span[class=author-born-location]")[0].text[3:]
    return birthday_date, born_location, description.strip()


def starts_with_author(href):
    return href and href.startswith("/author")


def collect_authors_on_page(session, page_url):
    response = session.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    div_class_quote = soup.find_all("div", class_="quote")
    for div in div_class_quote:
        author_link = base_url + div.find(
            "a", href=lambda href: href and "/author/" in href
        ).get("href")
        name_of_author = div.find("small", class_="author").text
        author = {}

        author["fullname"] = name_of_author
        (
            author["born_date"],
            author["born_location"],
            author["description"],
        ) = grab_autrhor_biography(session, author_link)

        quote = {}
        quote["tags"] = [tag.text for tag in div.find_all("a", class_="tag")]
        quote["author"] = name_of_author
        quote["quote"] = div.span.text
        qoutes.append(quote)

        if author not in authors:
            authors.append(author)


def collect_pages_urls(session, main_url):
    next_page = main_url
    while True:
        response = session.get(next_page)
        soup = BeautifulSoup(response.text, "html.parser")
        yield next_page
        next_link = soup.select_one("li.next a")
        if next_link is None:
            break
        next_page = main_url + next_link["href"]


if __name__ == "__main__":
    with requests.Session() as session:
        for page_url in collect_pages_urls(session, base_url):
            collect_authors_on_page(session, page_url)
        write_to_json("authors", authors)
        write_to_json("qoutes", qoutes)
    print(
        f"Parsing is complete. \nAuthors collected: {len(authors)} \nQuotes collected: {len(qoutes)}"
    )
