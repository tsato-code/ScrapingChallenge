import datetime
import os
import requests
import time
import urllib.parse

from bs4 import BeautifulSoup


OUT_DIR = "./dataset"
HOME_URL = "https://cookpad.com"


def crawling():
    os.makedirs(OUT_DIR, exist_ok=True)

    # キャラ弁のレシピを取得
    url = "https://cookpad.com/search/%E3%82%AD%E3%83%A3%E3%83%A9%E5%BC%81?order=popularity&page=1"
    response = requests.get(url)
    time.sleep(1)

    page_count = 1
    with open(os.path.join(OUT_DIR, f"page{page_count}.html"), "w", encoding="utf-8") as f:
        f.write(response.text)

    # 総レシピ数の取得
    soup = BeautifulSoup(response.content, "lxml")
    num_recipe = int(soup.find(class_="paginator").contents[1].text.split("/")[1].strip().replace(",", ""))
    print(f"キャラ弁の総レシピ数： {num_recipe}")

    # テキストファイルにキャラ弁数を保存
    with open(os.path.join(OUT_DIR, "data.txt"), "w") as f:
        f.write(f"{num_recipe}\n")

    # 2ページ目以降をクローリング
    while True:
        page_count += 1
        # next_url = soup.find("div", class_="paginator").contents[3:]
        next_url = soup.find("a", rel="next").attrs["href"]

        if next_url is None:
            print(f"総ページ数： {page_count-1}")
            with open(os.path.join(OUT_DIR, "data.txt"), mode="a") as f:
                f.write(f"{page_count-1}\n")
            break

        url = urllib.parse.urljoin(HOME_URL, next_url)
        response = requests.get(url)
        time.sleep(1)
        with open(os.path.join(OUT_DIR, f"page{page_count}.html"), "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.content, "lxml")
        if page_count % 10 == 0:
            print(f"{page_count}ページ取得")


def main():
    crawling()


if __name__ == "__main__":
    date_now = datetime.datetime.now()
    print(f"クローリング開始: {date_now}")
    main()
    date_now = datetime.datetime.now()
    print(f"クローリング終了: {date_now}")
