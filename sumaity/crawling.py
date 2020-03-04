import datetime
import os
import requests
import time

from bs4 import BeautifulSoup


OUT_DIR = "./dataset"


def crawling():
    os.makedirs(OUT_DIR, exist_ok=True)

    url = "https://sumaity.com/chintai/commute_list/list.php?position=&all_count=8255&sort1=8&sort2=&select_type=&search_type=c&q=&station_id%5B%5D=2174050&station_id%5B%5D=2196310&station_id%5B%5D=2325150&station_id%5B%5D=2174060&station_id%5B%5D=2174070&station_id%5B%5D=2196320&station_id%5B%5D=2175020&station_id%5B%5D=2196280&station_id%5B%5D=2174080&station_id%5B%5D=2373210&station_id%5B%5D=2175030&station_id%5B%5D=4001112&station_id%5B%5D=2331180&station_id%5B%5D=2174090&station_id%5B%5D=2175040&station_id%5B%5D=2171036&station_id%5B%5D=2174010&station_id%5B%5D=2196300&from_stid%5B%5D=2171036&cost_time%5B%5D=10&transit_count%5B%5D=&pref_id=13&view_type=3&create_date=&page_count=60&madori%5B%5D=1_10&madori%5B%5D=1_20&madori%5B%5D=1_30&madori%5B%5D=1_50&price_low=50000&price_high=100000"
    response = requests.get(url)
    time.sleep(1)

    page_count = 1
    with open(os.path.join(OUT_DIR, f"page{page_count}.html"), "w", encoding="utf-8") as f:
        f.write(response.text)

    # 総物件数の取得
    # print(response.content.decode("utf-8"))
    soup = BeautifulSoup(response.content, "lxml")
    num_bukken = int(soup.find(class_="searchResultHit").contents[1].text.replace(",", ""))
    print(f"通学時間60分以内の総物件数： {num_bukken}")

    # テキストファイルに物件数を保存
    with open(os.path.join(OUT_DIR, "data.txt"), "w") as f:
        f.write(f"{num_bukken}\n")

    # 2ページ目以降をクローリング
    while True:
        page_count += 1
        next_url = soup.find("li", class_="next")

        if next_url is None:
            print(f"総ページ数： {page_count-1}")
            with open(os.path.join(OUT_DIR, "data.txt"), mode="a") as f:
                f.write(f"{page_count-1}\n")
            break
        
        url = next_url.a.get("href")
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
    main()
