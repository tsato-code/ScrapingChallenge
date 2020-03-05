from logging import getLogger, StreamHandler, DEBUG, Formatter
from logging.handlers import TimedRotatingFileHandler
import argparse
import datetime
import os
import requests
import time
import urllib.parse

from bs4 import BeautifulSoup


OUT_DIR = "./dataset/carry"
HOME_URL = "https://cookpad.com"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, help="target url")
    parser.add_argument("-hu", "--home_url", type=str, help="home url")
    parser.add_argument("-o", "--out_dir", type=str, help="output directory")
    return parser.parse_args()


def crawling(args):
    OUT_DIR = args.out_dir
    HOME_URL = args.home_url
    url = args.url

    # レシピを取得
    response = requests.get(url)
    time.sleep(1)

    page_count = 1
    with open(os.path.join(OUT_DIR, f"page{page_count:000006}.html"), "w", encoding="utf-8") as f:
        f.write(response.text)

    # 総レシピ数の取得
    soup = BeautifulSoup(response.content, "lxml")
    num_recipe = int(soup.find(class_="paginator").contents[1].text.split("/")[1].strip().replace(",", ""))
    print(f"総レシピ数： {num_recipe}")

    # テキストファイルにキャラ弁数を保存
    with open(os.path.join(OUT_DIR, "data.txt"), "w") as f:
        f.write(f"{num_recipe}\n")

    # 2ページ目以降をクローリング
    while True:
        page_count += 1
        next_url = soup.find("a", rel="next")

        if next_url is None:
            print(f"総ページ数： {page_count-1}")
            with open(os.path.join(OUT_DIR, "data.txt"), mode="a") as f:
                f.write(f"{page_count-1}\n")
            break

        url = urllib.parse.urljoin(HOME_URL, next_url.attrs["href"])

        # 取得できるまで繰り返し
        for _i in range(1000):
            try:
                response = requests.get(url)
                time.sleep(1)
                break
            except Exception as e:
                print(e)
                time.sleep(10)

        with open(os.path.join(OUT_DIR, f"page{page_count:000006}.html"), "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.content, "lxml")
        if page_count % 10 == 0:
            print(f"{page_count}ページ取得")


def main():
    args = get_args()
    print(args)
    os.makedirs(args.out_dir, exist_ok=True)
    crawling(args)


if __name__ == "__main__":
    logger = getLogger(None)

    fmt_text = (
        "%(asctime)s %(name)s %(lineno)d"
        " [%(levelname)s][%(funcName)s] %(message)s"
    )
    log_fmt = Formatter(fmt_text)

    handler = StreamHandler()
    handler.setLevel("INFO")
    handler.setFormatter(log_fmt)
    logger.setLevel("INFO")
    logger.addHandler(handler)

    logdir, logfile = os.path.split(os.path.abspath(__file__))
    logpath = logfile + ".log"
    handler = TimedRotatingFileHandler(
        filename=logpath,
        when="D",
        backupCount=7
    )
    handler.setLevel(DEBUG)
    handler.setFormatter(log_fmt)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)

    date_now = datetime.datetime.now()
    print(f"クローリング開始: {date_now}")
    main()
    date_now = datetime.datetime.now()
    print(f"クローリング終了: {date_now}")
