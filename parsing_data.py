import requests
import json
import asyncio

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from time import time
from async_timer import async_timer

PAGES = 10
base_url = "https://quotes.toscrape.com"
url = "https://quotes.toscrape.com/page/"
page = 1


def check_page_exists(url: str) -> bool:
    response = requests.get(url)
    return response.status_code == 200


def scrape_page_data(full_url: str) -> None:
    des_url = []
    quotes_all = []
    authors_all = []
    tags_all = []

    if not check_page_exists(full_url):
        print(f"Page {full_url} does not exist.")
        return

    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.select("div[class=quote] span[class=text]")
    for quote in quotes:
        quotes_all.append(quote.get_text().strip("\u201c, \u201d"))

    authors = soup.select("div[class=quote] span small[class=author]")
    for author in authors:
        authors_all.append(author.get_text())

    div_tags = soup.find_all("div", class_="tags")
    for div_tag in div_tags:
        tag_list = div_tag.find_all("a", class_="tag")
        tags_of_author = []
        for tag in tag_list:
            tags_of_author.append(tag.get_text())
        tags_all.append(tags_of_author)

    authors_des_url = soup.select("div[class=quote] span a")

    for author in authors_des_url:
        des_url.append(author.get("href"))

    data = create_quote_data_structure(quotes_all, authors_all, tags_all)
    return data, des_url


@async_timer()
async def fetch_quotes_async(url: str) -> list:
    loop = asyncio.get_running_loop()

    full_urls = [url + str(page) for page in range(1, PAGES + 1)]

    info_quotes = []
    descriptions_link = []

    with ThreadPoolExecutor(10) as pool:
        futures = [loop.run_in_executor(pool, scrape_page_data, url) for url in full_urls]
        queues = await asyncio.gather(*futures, return_exceptions=True)
        for gather in queues:
            info_quotes.extend(gather[0])
            descriptions_link.extend(gather[1])
    return info_quotes, descriptions_link


def create_quote_data_structure(quotes_all: list, authors_all: list, tags_all: list) -> list:
    data = []
    for quote, author, tag in zip(quotes_all, authors_all, tags_all):
        data.append({"tags": tag, "author": author, "quote": quote})

    return data


def make_json_quotes(quotes_info: list) -> None:
    with open("quotes.json", "w", encoding="utf-8") as json_file:
        json.dump(quotes_info, json_file, indent=4, ensure_ascii=False)


def scrape_data_author(url: str) -> dict:
    if not check_page_exists(url):
        print(f"Page {url} does not exist.")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    full_name = soup.select("h3[class=author-title]")[0].get_text()

    born_date = soup.select("span[class=author-born-date]")[0].get_text()

    born_location = soup.select("span[class=author-born-location]")[0].get_text()

    description = soup.select("div[class=author-description]")[0].get_text().strip("\n").strip()

    info = {"fullname": full_name, "born_date": born_date, "born_location": born_location, "description": description}

    return info


@async_timer()
async def fetch_authors_async(des_url: list, base_url: str) -> list:
    loop = asyncio.get_running_loop()
    filter_des_url = list(set(des_url))

    full_urls = [base_url + url for url in filter_des_url]

    info_authors = []

    with ThreadPoolExecutor(50) as pool:
        futures = [loop.run_in_executor(pool, scrape_data_author, url) for url in full_urls]
        queues = await asyncio.gather(*futures, return_exceptions=True)
        for result in queues:
            info_authors.append(result)
    return info_authors


def make_json_authors(authors_info) -> None:
    with open("authors.json", "w", encoding="utf-8") as json_file:
        json.dump(authors_info, json_file, indent=4, ensure_ascii=False)


def main() -> None:
    quotes_info, des_url = asyncio.run(fetch_quotes_async(url))

    authors_info = asyncio.run(fetch_authors_async(des_url, base_url))

    make_json_authors(authors_info)

    make_json_quotes(quotes_info)


if __name__ == "__main__":
    start = time()
    main()
    print(time() - start)
